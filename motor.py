#Stepper motor (Nema 17) functions
from time import sleep
import RPi.GPIO as GPIO

SPR_Full_Step = 200   # Steps per Revolution for Nema 17 stepper motor
delay_s = 1.0/SPR_Full_Step/16.0 #the smaller the delay, the faster them motor turns

GPIO.setmode(GPIO.BCM)

DIR_MOTOR_X = 20    #X axis motor direction GPIO Pin
STEP_X = 21  # Step GPIO Pin
GPIO.setup(DIR_MOTOR_X, GPIO.OUT)
GPIO.setup(STEP_X, GPIO.OUT)

DIR_MOTOR_Y = 15  #Y axis motor direction GPIO Pin
STEP_Y = 14  # Step GPIO Pin
GPIO.setup(DIR_MOTOR_Y, GPIO.OUT)
GPIO.setup(STEP_Y, GPIO.OUT)

g_forceX = 0
g_forceFractionX = 0
g_forceY = 0
g_forceFractionY = 0
def setForce(forceX, forceFractionX, forceY, forceFractionY):
    global g_forceX, g_forceFractionX, g_forceY, g_forceFractionY
    forceX = g_forceX
    forceFractionX = g_forceFractionX
    forceY = g_forceY
    forceFractionY = g_forceFractionY

#map force to steps using linear interpolation. The larger the force, the more the steps
def calcStepCount(forceFraction):
    minSteps = 1
    maxSteps = 2*SPR_Full_Step
    return minSteps + int(round((maxSteps-minSteps)*forceFraction))

def moveMotorX():
    if g_forceFractionX > 0.05:
        steps = calcStepCount(g_forceFractionX)
        GPIO.output(DIR_MOTOR_X, g_forceX > 0)
        for _ in range(steps):
            GPIO.output(STEP_X, GPIO.HIGH)
            sleep(delay_s)
            GPIO.output(STEP_X, GPIO.LOW)
            sleep(delay_s)
        sleep(0.1)

def moveMotorY():
    if g_forceFractionY > 0.05:
        steps = calcStepCount(g_forceFractionY)
        GPIO.output(DIR_MOTOR_Y, g_forceY > 0)
        for _ in range(steps):
            GPIO.output(STEP_Y, GPIO.HIGH)
            sleep(delay_s)
            GPIO.output(STEP_Y, GPIO.LOW)
            sleep(delay_s)
        sleep(0.1)

def GPIOCleanup():
    GPIO.cleanup() # resets any ports you have used in this program back to input mode