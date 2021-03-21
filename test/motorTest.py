#https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/
#Stepper motor (Nema 17) test with Raspberry Pi
from time import sleep
import RPi.GPIO as GPIO

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
#SPR_Full_Step = 48   # Steps per Revolution (360 / 7.5)
SPR_Full_Step = 200   # Steps per Revolution for Nema 17 stepper motor for full step reolution

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

GPIO.output(MODE, RESOLUTION['Full'])
step_count = SPR_Full_Step * 1
delay = 1.0 / SPR_Full_Step / 1

GPIO.output(DIR, CW)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

sleep(.5)
GPIO.output(DIR, CCW)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()