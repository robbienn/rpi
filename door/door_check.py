import sys
import time
import datetime
import RPi.GPIO as GPIO
import tm1637
import http.client, urllib
import board
import adafruit_sht31d


MAX_CNT = 30
LOOP_SLEEP = 950/1000
TEMP_SHOW_SLEEP = 2

MIN_UPLOAD_TIME_DELTA = 15

EVENT_DOOR_CLOSED = "CLOSED"
EVENT_DOOR_OPENED= "OPENED"

NOTE_DURATION = 0.15

SPEAKERPORT = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKERPORT, GPIO.OUT)


# Thingspeak
SERVER_URL = "api.thingspeak.com:80"
channel_id = 685565
write_key  = "B9EK6TIS4WFTU5K2"


# Number of steps from A3. Font: http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html
NOTES = {
'A2': -12.0, 'Bb2': -11.0, 'B2': -10.0, 'C3': -9.0, 'Db3': -8.0, 'D3': -7.0, 
'Eb3': -6.0, 'E3': -5.0, 'F3': -4.0, 'Gb3': -3.0, 'G3': -2.0, 'Ab3': -1.0, 
'A3': 0.0, 'Bb3': 1.0, 'B3': 2.0, 'C4': 3.0, 'Db4': 4.0, 'D4': 5.0, 'Eb4': 6.0, 
'E4': 7.0, 'F4': 8.0, 'Gb4': 9.0, 'G4': 10.0, 'Ab4': 11.0, 'A4': 12.0, 'Bb4': 13.0, 
'B4': 14.0, 'C5': 15.0, 'Db5': 16.0, 'D5': 17.0, 'Eb5': 18.0, 'E5': 19.0, 'F5': 20.0, 'Gb5': 21.0, 'G5': 22.0, 'Ab5': 23.0}

DIO = 24
CLK = 23
tm = tm1637.TM1637(clk=CLK, dio=DIO)
tm.brightness(1)

# door magnet
# GPIO.setmode(GPIO.BOARD)
DOOR_MAGNET_PIN = 14
GPIO.setup(DOOR_MAGNET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)



#Display.Show([0x7f, 0,0,0])
#time.sleep(3)

################################################################################

def tone(note, duration):
    
    # Font: http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html
    frequency = 440.0 * (1.05946309435929530984310531 ** NOTES[note])
    
    p = GPIO.PWM(SPEAKERPORT, frequency)    # 50 Hertz PWM
    p.start(50) #Duty cycle: 50%
    time.sleep(duration)
    p.stop()
    time.sleep(0.01)

def openedSound():
    tone('C3', NOTE_DURATION)
    tone('D3', NOTE_DURATION)
    tone('E3', NOTE_DURATION)
    #tone('F3', NOTE_DURATION)
    #tone('G3', NOTE_DURATION)


def closedSound():
    #tone('G3', NOTE_DURATION)
    #tone('F3', NOTE_DURATION)
    tone('E3', NOTE_DURATION)
    tone('D3', NOTE_DURATION)
    tone('C3', NOTE_DURATION)


'''
def prepareNumber(number):
    result = [];
    leading = True
    last4 = str(number)[-4:].rjust(4,'0')
    for d in str(last4):
        if (d == "0") and leading:
            result.append(0x7f)
        else:
            leading = False
            result.append(int(d))
    return result
'''

def showTime():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    global showColon
    showColon = not showColon
    tm.numbers(hour, minute, showColon)
    time.sleep(1)


def showCountDown(seconds):
    for i in range(seconds, -1, -1):
        tm.number(i)
        time.sleep(1)


def getDuration(startTime, endTime):
    duration = endTime - startTime
    seconds = duration.seconds
    return seconds

def showDuration(seconds):    
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    global showColon
    showColon = not showColon
    print("H,M,S:", h,m,s)    

    if h>0:
        tm.numbers(h,m,showColon)
    else:
        tm.numbers(m,s,showColon)


def showTemperature():
    tm.temperature(round(getTemperature()))
    time.sleep(TEMP_SHOW_SLEEP)

        

def isDoorOpen():    
    if GPIO.input(DOOR_MAGNET_PIN):
        #print("Door is open")
        result = True
    else:
        result = False
        #print("Door is closed")
    return result


def getTemperature():
    return round(sensor.temperature, 1)

def getHumidity():
    return round(sensor.relative_humidity, 1)


def uploadToThingSpeak(event, timestamp, duration, temperature, humidity):

        #to_log = str(timestamp) + ' - T1={0:0.1f}*C H={1:0.1f}% P={2:0.1f} T2={3:0.1f}*C'.format(temperature, humidity, pressure, temperature2)

        now = datetime.datetime.now()

        global lastTimeUpload

        if lastTimeUpload is not None:
            delta = getDuration(lastTimeUpload, now)
            print("Seconds between uploads", delta)
            if delta < MIN_UPLOAD_TIME_DELTA:
                timeToSleep = MIN_UPLOAD_TIME_DELTA - delta
                print("Sleep before upload to thingspeak: ", timeToSleep)
                showCountDown(timeToSleep)         

        params = urllib.parse.urlencode(
                {'field1': event, 'field2': timestamp, 'field3': duration, 'field7': temperature, 'field8': humidity, 'key': write_key})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection(SERVER_URL)
        try:
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                print (response.status, response.reason)
                data = response.read()
                conn.close()
                #to_log += " - " + str(response.status) + " " + str(response.reason)
        except:
                #to_log += " - Connection to " + SERVER_URL + " failed!"
                print("POST error")


        lastTimeUpload = now

        #print(to_log)
        #logging.info(to_log)




#################################################################################

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

showColon = False
loopCounter = 0

lastTimeUpload = None

'''
for i in range(128):
    tm.number(i)
    tm.write([i])
    time.sleep(0.1)
'''

now = datetime.datetime.now()
print(now)
print("--------------------------------")
print("\nTemperature: %0.1f C" % sensor.temperature)
print("Humidity: %0.1f %%" % sensor.relative_humidity)

isOpened = isDoorOpen()
if isOpened:
    doorOpenedAt = now
    doorClosedAt = None
    print("Initial status: OPENED")
else:
    doorClosedAt = now
    doorOpenedAt = None
    print("Initial status: CLOSED")

while True:
    loopCounter += 1
    now = datetime.datetime.now()
    wasOpened = isOpened
    isOpened = isDoorOpen()

    if loopCounter == MAX_CNT:
        loopCounter = 0
        showTemperature()

    if not isOpened:
        if wasOpened:
            doorClosedAt = datetime.datetime.now()
            dca = doorClosedAt.strftime("%Y-%m-%d_%H:%M:%S")
            print("Dvere zavreny v:", dca)

            #closedSound()
            duration = getDuration(doorOpenedAt, doorClosedAt)
            print("Doba otevreni: ", duration)

            uploadToThingSpeak(EVENT_DOOR_CLOSED, dca, duration, getTemperature(), getHumidity())
            print("KONEC UPLOADU")

        else:
            showTime()

    if isOpened:
        if not wasOpened:
            doorOpenedAt = datetime.datetime.now()
            doa = doorOpenedAt.strftime("%Y-%m-%d_%H:%M:%S")
            print("Dvere otevreny v:", doa)

            #openedSound()
            duration = getDuration(doorClosedAt, doorOpenedAt)
            print("Doba zavreni: ", duration)

            uploadToThingSpeak(EVENT_DOOR_OPENED, doa, duration, getTemperature(), getHumidity())
            print("KONEC UPLOADU")
        else:
            showDuration(getDuration(doorOpenedAt, now))
  

    time.sleep(LOOP_SLEEP)


print("--------------------------------")

