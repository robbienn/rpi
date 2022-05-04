import sys
import time
import datetime
import RPi.GPIO as GPIO
import http.client, urllib
import board
import adafruit_sht31d
import logging

LOOP_SLEEP = 60*5 # in seconds

LOCATION_FILE = "/home/pi/location"

# Thingspeak
SERVER_URL = "api.thingspeak.com:80"
channel_id = 685565
write_key  = "ZIVF3B55MTQJR5SY"

################################################################################

def getLocation():

    #LOCATION = "OP" # obyvaci pokoj
    #LOCATION = "PR" # predsin
    #LOCATION = "LD" # lodzie
    #LOCATION = "DP" # detsky pokoj

    f = open(LOCATION_FILE, "r")
    return (f.readline().strip())

def getTemperature():
    return round(sensor.temperature, 1)

def getHumidity():
    return round(sensor.relative_humidity, 1)

def uploadToThingSpeak(temperature, humidity,):

        #to_log = str(timestamp) + ' - T1={0:0.1f}*C H={1:0.1f}% P={2:0.1f} T2={3:0.1f}*C'.format(temperature, humidity, pressure, temperature2)

        now = datetime.datetime.now()

        if (LOCATION == "OP"):
            params = urllib.parse.urlencode( {'field1': temperature, 'field2': humidity, 'key': write_key} )
        elif (LOCATION == "PR"):
            params = urllib.parse.urlencode( {'field3': temperature, 'field4': humidity, 'key': write_key} )
        elif (LOCATION == "LD"):
            params = urllib.parse.urlencode( {'field5': temperature, 'field6': humidity, 'key': write_key} )
        elif (LOCATION == "DP"):
            params = urllib.parse.urlencode( {'field7': temperature, 'field8': humidity, 'key': write_key} )
        else:
            logging.error("WRONG LOCATION")
            return -1

        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection(SERVER_URL)
        try:
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                logging.info("Response: %s %s", response.status, response.reason)
                data = response.read()
                conn.close()
                #to_log += " - " + str(response.status) + " " + str(response.reason)
        except:
                #to_log += " - Connection to " + SERVER_URL + " failed!"
                logging.error("POST error")



#################################################################################

# Create sensor object, communicating over the board's default I2C bus
logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s %(levelname)s %(message)s', 
        handlers=[logging.FileHandler('home_temp_humi.log'), logging.StreamHandler()]
)
logging.info("=======================================")
logging.info("HOME TEMP HUMI - START")

i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

LOCATION = getLocation()
logging.info("LOCATION: %s", LOCATION)

while True:

    temp = round(sensor.temperature, 1)
    humi = round(sensor.relative_humidity, 1)

    now = datetime.datetime.now()
    logging.info("Temperature: %0.1f C" % temp)
    logging.info("Humidity: %0.1f %%" % humi)

    sensor.heater = True
    logging.debug("Sensor Heater status = %s", sensor.heater)
    time.sleep(1)
    sensor.heater = False
    logging.debug("Sensor Heater status = %s", sensor.heater)

    uploadToThingSpeak(temp, humi)

    time.sleep(LOOP_SLEEP)

logging.info("HOME TEMP HUMI - END")
