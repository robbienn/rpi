from datetime import datetime

import time
import board
import adafruit_sht31d

from board import SCL, SDA
import busio

from PIL import Image, ImageDraw, ImageFont

import adafruit_ssd1306
import digitalio

import adafruit_bmp280

LOOP_DELAY_SECS = 60

OLED_X_SIZE = 128
OLED_Y_SIZE = 32

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()
sht3 = adafruit_sht31d.SHT31D(i2c)

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
bmp280.sea_level_pressure = 1013.25


RESET_PIN = digitalio.DigitalInOut(board.D4)
i2c_oled = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(OLED_X_SIZE, OLED_Y_SIZE, i2c_oled, addr=0x3C, reset=RESET_PIN)
display.fill(0)
display.show()




'''
for y in range(OLED_Y_SIZE):
    for x in range(OLED_X_SIZE):
        display.pixel(x, y, 1)
    display.show()
'''

#font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
#font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 8)
#font = ImageFont.load_default()
#font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansTelugu-Bold.ttf", 12)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)




loopcount = 0
while True:
    loopcount += 1

    image = Image.new("1", (display.width, display.height))
    draw = ImageDraw.Draw(image)

    now = datetime.now()
    datetime_str = now.strftime("%d.%m.%Y - %H:%M:%S")

    temp = round(sht3.temperature, 1)
    temp_str = str(temp) + chr(176)

    humi = round(sht3.relative_humidity, 1)
    humi_str = str(humi) + "%"

    temp_humi_str = temp_str + " - " + humi_str


    print("SHT3 Temperature: %0.1f C" % bmp280.temperature)
    print("SHT3 Pressure: %0.1f hPa" % bmp280.pressure)
    print("SHT3 Altitude = %0.2f meters" % bmp280.altitude)


    print("Timestamp =", datetime_str) 
    print("Temperature = ", temp_str)
    print("Humidity = ", humi_str)
    print("----------------------------------\n")




    display.fill(0)
    display.show()

    draw.text((0, 5), datetime_str, font=font, fill=255)
    draw.text((0, 18), temp_humi_str, font=font2, fill=255)
    
    display.image(image)
    display.show()

    for x in range(OLED_X_SIZE):
        display.pixel(x, 1, 1)
        display.pixel(x, 2, 1)
        display.pixel(x, 3, 1)
        display.pixel(x, 4, 1)
        display.show()
        time.sleep(0.5)

    if loopcount == 10:
        loopcount = 0
        sht3.heater = True
        print("Sensor Heater status =", sht3.heater)
        time.sleep(1)
        sht3.heater = False
        print("Sensor Heater status =", sht3.heater)




