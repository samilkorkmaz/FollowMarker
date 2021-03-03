#https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/
#Stepper motor (Nema 17) test with Raspberry Pi
from time import sleep
import RPi.GPIO as GPIO

SPR_Full_Step = 200   # Steps per Revolution for Nema 17 stepper motor for full step reolution
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
GPIO.setmode(GPIO.BCM)

DIR_MOTOR_X = 20    #X axis motor direction GPIO Pin
STEP_X = 21  # Step GPIO Pin
MODE_X = (14, 15, 18)   # Microstep Resolution GPIO Pins
GPIO.setup(DIR_MOTOR_X, GPIO.OUT)
GPIO.setup(STEP_X, GPIO.OUT)
GPIO.setup(MODE_X, GPIO.OUT)

DIR_MOTOR_Y =     #Y axis motor direction GPIO Pin
STEP_Y =   # Step GPIO Pin
MODE_Y = (, , )   # Microstep Resolution GPIO Pins
GPIO.setup(DIR_MOTOR_Y, GPIO.OUT)
GPIO.setup(STEP_Y, GPIO.OUT)
GPIO.setup(MODE_Y, GPIO.OUT)

#map force to delay using linear interpolation
minDelay_s = 1.0 / SPR_Full_Step / 32
maxDelay_s = 1.0 / SPR_Full_Step / 1
def calcDelay_s(forceFraction, mode):
    global minDelay_s, maxDelay_s, GPIO, RESOLUTION
    delay_s = minDelay_s + (maxDelay_s - minDelay_s) * abs(forceFraction)
    if delay_s < 1.0/16.0:
        GPIO.output(mode, RESOLUTION['1/32'])
        return 1.0/32.0
    elif  delay_s < 1.0/8.0:
        GPIO.output(mode, RESOLUTION['1/16'])
        return 1.0/16.0
    elif delay_s < 1.0/4.0:
        GPIO.output(mode, RESOLUTION['1/8'])
        return 1.0/8.0
    elif delay_s < 1.0/2.0:
        GPIO.output(mode, RESOLUTION['1/4'])
        return 1.0/4.0
    elif delay_s < 1.0:
        GPIO.output(mode, RESOLUTION['Half'])
        return 1.0/2.0
    else:
        GPIO.output(mode, RESOLUTION['Full'])
        return 1.0

def moveMotorXOneStep(forceFraction):
    global MODE_X, GPIO, DIR_MOTOR_X, STEP_X
    delay_s = calcDelay_s(forceFraction, MODE_X)
    GPIO.output(DIR_MOTOR_X, forceFraction > 0)
    GPIO.output(STEP_X, GPIO.HIGH)
    sleep(delay_s)
    GPIO.output(STEP_X, GPIO.LOW)
    sleep(delay_s)

def moveMotorYOneStep(forceFraction):
    global MODE_Y, GPIO, DIR_MOTOR_Y, STEP_Y
    delay_s = calcDelay_s(forceFraction, MODE_Y)
    GPIO.output(DIR_MOTOR_Y, forceFraction > 0)
    GPIO.output(STEP_Y, GPIO.HIGH)
    sleep(delay_s)
    GPIO.output(STEP_Y, GPIO.LOW)
    sleep(delay_s)

def GPIOCleanup():
    GPIO.cleanup()