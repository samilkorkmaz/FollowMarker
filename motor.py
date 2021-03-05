#https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/
#Stepper motor (Nema 17) test with Raspberry Pi
from time import sleep
import RPi.GPIO as GPIO

SPR_Full_Step = 200   # Steps per Revolution for Nema 17 stepper motor for full step reolution
delay_s = 1.0/SPR_Full_Step/16.0 #the smaller the delay, the faster them motor turns
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
GPIO.setmode(GPIO.BCM)

DIR_MOTOR_X = 20    #X axis motor direction GPIO Pin
STEP_X = 21  # Step GPIO Pin
MICROSTEP_X = (14, 15, 18)   # Microstep Resolution GPIO Pins
GPIO.setup(DIR_MOTOR_X, GPIO.OUT)
GPIO.setup(STEP_X, GPIO.OUT)
GPIO.setup(MICROSTEP_X, GPIO.OUT)
GPIO.output(MICROSTEP_X, RESOLUTION['Full'])

'''DIR_MOTOR_Y =     #Y axis motor direction GPIO Pin
STEP_Y =   # Step GPIO Pin
MICROSTEP_Y = (, , )   # Microstep Resolution GPIO Pins
GPIO.setup(DIR_MOTOR_Y, GPIO.OUT)
GPIO.setup(STEP_Y, GPIO.OUT)
GPIO.setup(MODE_Y, GPIO.OUT)
GPIO.output(MICROSTEP_Y, RESOLUTION['Full'])'''

#map force to steps using linear interpolation. The larger the force, the more the steps
def calcStepCount(forceFraction):
    minSteps = 1
    maxSteps = 2*SPR_Full_Step
    return minSteps + int(round((maxSteps-minSteps)*forceFraction))

def moveMotorXOneStep(forceFraction, direction):
    steps = calcStepCount(forceFraction)
    GPIO.output(DIR_MOTOR_X, direction)
    for _ in range(steps):
        GPIO.output(STEP_X, GPIO.HIGH)
        sleep(delay_s)
        GPIO.output(STEP_X, GPIO.LOW)
        sleep(delay_s)

'''def moveMotorYOneStep(forceFraction, direction):
    steps = calcStepCount(forceFraction)
    GPIO.output(DIR_MOTOR_Y, direction)
    for i in range(steps):
        GPIO.output(STEP_Y, GPIO.HIGH)
        sleep(delay_s)
        GPIO.output(STEP_Y, GPIO.LOW)
        sleep(delay_s)'''

def GPIOCleanup():
    GPIO.cleanup() # resets any ports you have used in this program back to input mode