import RPi.GPIO as GPIO
import time

# rpi-pcspeaker by jsubirat
#
# Connections:
#       * Speaker + - GPIO 23 (can be modified in SPEAKERPORT variable)
#       * Speaker - - GND
#
# The polarity doesn't matter as long as it is a classical PC speaker. Note that GPIO v0.5.2a is required to have software-PWM.

# GPIO speaker output port in the BCM numbering scheme. You can choose any appropiate output port.
SPEAKERPORT = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKERPORT, GPIO.OUT)

# Number of steps from A3. Font: http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html
NOTES = {
'A2': -12.0, 'Bb2': -11.0, 'B2': -10.0, 'C3': -9.0, 'Db3': -8.0, 'D3': -7.0, 
'Eb3': -6.0, 'E3': -5.0, 'F3': -4.0, 'Gb3': -3.0, 'G3': -2.0, 'Ab3': -1.0, 
'A3': 0.0, 'Bb3': 1.0, 'B3': 2.0, 'C4': 3.0, 'Db4': 4.0, 'D4': 5.0, 'Eb4': 6.0, 
'E4': 7.0, 'F4': 8.0, 'Gb4': 9.0, 'G4': 10.0, 'Ab4': 11.0, 'A4': 12.0, 'Bb4': 13.0, 
'B4': 14.0, 'C5': 15.0, 'Db5': 16.0, 'D5': 17.0, 'Eb5': 18.0, 'E5': 19.0, 'F5': 20.0, 'Gb5': 21.0, 'G5': 22.0, 'Ab5': 23.0}

# Key to note mapping
KEYS = {'z': 'A2', 's': 'Bb2', 'x': 'B2', 'c': 'C3', 'f': 'Db3', 'v': 'D3', 'g': 'Eb3', 'b': 'E3', 'n': 'F3', 'j': 'Gb3', 'm': 'G3', 'k': 'Ab3', 'q': 'A3', '2': 'Bb3', 'w': 'B3', 'e': 'C4', '4': 'Db4', 'r': 'D4', '5': 'Eb4', 't': 'E4', 'y': 'F4', '7': 'Gb4', 'u': 'G4', '8': 'Ab4', 'i': 'A4', '9': 'Bb4', 'o': 'B4', 'p': 'C5'} #etc.

# Sets the desired note at the speaker
def tone(note, duration):
    
    # Font: http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html
    frequency = 440.0 * (1.05946309435929530984310531 ** NOTES[note])
    
    p = GPIO.PWM(SPEAKERPORT, frequency)    # 50 Hertz PWM
    p.start(50) #Duty cicle: 50%
    time.sleep(duration)
    p.stop()
    time.sleep(0.1)

def play_all_notes():
	for note in NOTES:
		print("NOTE: ", note)
		tone(note, 1)
		time.sleep(1)

def up_and_down():
	tone('C3', 0.3)
	tone('E3', 0.3)
	tone('F3', 0.3)
	tone('E3', 0.3)
	tone('C3', 0.3)

def kocka_leze_dirou():
	tone('C3', 0.4)
	tone('D3', 0.4)
	tone('E3', 0.4)
	tone('F3', 0.4)
	tone('G3', 0.6)
	tone('G3', 0.6)
	tone('A3', 0.4)
	tone('A3', 0.4)
	tone('G3', 0.4)
	time.sleep(0.3)
	tone('A3', 0.4)
	tone('A3', 0.4)
	tone('G3', 0.4)


# Main code


play_all_notes()
up_and_down()
kocka_leze_dirou()






'''
key = ''
while key != ' ':
    key = input('Enter a note: ')
    if key in KEYS.keys():
        tone(SPEAKERPORT, KEYS[key])
    else:
        if key == ' ':
            break
        else:
            print("Invalid note (space to exit)!")
'''


GPIO.cleanup()



'''


import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  
GPIO.setup(17, GPIO.OUT)# set GPIO 25 as an output. You can use any GPIO port  
p = GPIO.PWM(17, 50)    # create an object p for PWM on port 25 at 50 Hertz  
'''

'''
p.start(70)             # start the PWM on 70 percent duty cycle  
for x in range(200, 2200):
	p.ChangeFrequency(x)  # change the frequency to x Hz (
	time.sleep(0.0001)


'''
'''

p.start(0)
for dc in range(0, 101, 5):
	p.ChangeDutyCycle(dc)
	time.sleep(0.1)
'''


'''
for freq in range(5000, 20000, 10):
	p.ChangeFrequency(freq)
	time.sleep(1)
	'''

'''
for dc in range(100, -1, -5):
	p.ChangeDutyCycle(dc)
	time.sleep(0.1)
	'''
'''
p.stop()                # stop the PWM output  
GPIO.cleanup()          # when your program exits, tidy up after yourself
'''