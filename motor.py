#https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/
#Stepper motor (Nema 17) test with Raspberry Pi
from time import sleep
import RPi.GPIO as GPIO

DIR_MOTOR_X = 20    #X axis motor direction GPIO Pin
DIR_MOTOR_Y = ???   #Y axis motor direction GPIO Pin

STEP = 21  # Step GPIO Pin
MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
SPR_Full_Step = 200   # Steps per Revolution for Nema 17 stepper motor for full step reolution

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_MOTOR_X, GPIO.OUT)
GPIO.setup(DIR_MOTOR_Y, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

GPIO.output(MODE, RESOLUTION['Full'])

#map force to delay using linear interpolation
minDelay_s = 1.0 / SPR_Full_Step / 32
maxDelay_s = 1.0 / SPR_Full_Step / 1
def calcDelay_s(minForce, maxForce, force):
    global minDelay_s, maxDelay_s
    return minDelay_s + force * (maxDelay_s - minDelay_s) / (maxForce - minForce)

def moveMotor(delay_s, steps):
    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay_s)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay_s)

def moveMotorOneStep(delay_s):
    moveMotor(delay_s, 1)

def moveMotorXOneStep(delay_s, direction):
    GPIO.output(DIR_MOTOR_X, direction)
    moveMotorOneStep(delay_s, direction)

def moveMotorYOneStep(delay_s, direction):
    GPIO.output(DIR_MOTOR_Y, direction)
    moveMotorOneStep(delay_s, direction)

def GPIOCleanup():
    GPIO.cleanup()