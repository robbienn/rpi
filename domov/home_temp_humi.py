import sys
import time
import datetime
import RPi.GPIO as GPIO
import http.client, urllib
import board
import adafruit_sht31d

# Thingspeak

LOOP_SLEEP = 60*5 # in seconds

LOCATION = "OP" # obyvaci pokoj
#LOCATION = "PR" # predsin

SERVER_URL = "api.thingspeak.com:80"
channel_id = 685565
write_key  = "ZIVF3B55MTQJR5SY"

################################################################################
def getTemperature():
    return round(sensor.temperature, 1)

def getHumidity():
    return round(sensor.relative_humidity, 1)


def uploadToThingSpeak(temperature, humidity):

        #to_log = str(timestamp) + ' - T1={0:0.1f}*C H={1:0.1f}% P={2:0.1f} T2={3:0.1f}*C'.format(temperature, humidity, pressure, temperature2)

        now = datetime.datetime.now()

        if (LOCATION == "OP"):
            params = urllib.parse.urlencode( {'field1': temperature, 'field2': humidity, 'key': write_key} )
        elif (LOCATION == "PR"):
            params = urllib.parse.urlencode( {'field3': temperature, 'field4': humidity, 'key': write_key} )
        else:
            print("WRONG LOCATION")
            return -1

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


        #print(to_log)
        #logging.info(to_log)




#################################################################################

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

while True:

    temp = round(sensor.temperature, 1)
    humi = round(sensor.relative_humidity, 1)

    now = datetime.datetime.now()
    print("Timestamp: ", now)
    print("Location: ", LOCATION)
    print("\nTemperature: %0.1f C" % temp)
    print("Humidity: %0.1f %%" % humi)
    print("-----------")

    sensor.heater = True
    print("Sensor Heater status =", sensor.heater)
    time.sleep(1)
    sensor.heater = False
    print("Sensor Heater status =", sensor.heater)
    print("--------------------------------")

    uploadToThingSpeak(temp, humi)

    time.sleep(LOOP_SLEEP)


