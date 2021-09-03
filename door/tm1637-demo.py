import tm1637
import time

DIO = 24
CLK = 23

print("TM 1637 test - begin")

tm = tm1637.TM1637(clk=CLK, dio=DIO)

tm.brightness(1)

# all LEDS on "88:88"
tm.write([127, 255, 127, 127])
time.sleep(2)

# all LEDS off
tm.write([0, 0, 0, 0])
time.sleep(2)

# show "0123"
tm.write([63, 6, 91, 79])
time.sleep(2)

# show "COOL"
tm.write([0b00111001, 0b00111111, 0b00111111, 0b00111000])
time.sleep(2)

# show "HELP"
tm.show('help')
time.sleep(2)

# display "dEAd", "bEEF"
tm.hex(0xdead)
time.sleep(2)

tm.hex(0xbeef)
time.sleep(2)

# show "12:59"
tm.numbers(12, 59)
time.sleep(2)

# show "-123"
tm.number(-123)
time.sleep(2)

# show temperature '24*C'
tm.temperature(24)
time.sleep(2)

print("TM 1637 test - end")