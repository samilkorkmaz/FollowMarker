#Stepper motor (Nema 17) functions
from time import sleep
import RPi.GPIO as GPIO

class MotorNema:
    def __init__(self):
        self.keepRunning = True        
        self.SPR_Full_Step = 200   # Steps per Revolution for Nema 17 stepper motor
        self.delay_s = 1.0/self.SPR_Full_Step/2 #the smaller the delay, the faster them motor turns
        self.g_forceX = 0
        self.g_forceFractionX = 0
        self.g_forceY = 0
        self.g_forceFractionY = 0
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.DIR_MOTOR_X = 20    #X axis motor direction GPIO Pin
        self.STEP_X = 21  # Step GPIO Pin
        GPIO.setup(self.DIR_MOTOR_X, GPIO.OUT)
        GPIO.setup(self.STEP_X, GPIO.OUT)

        self.DIR_MOTOR_Y = 15  #Y axis motor direction GPIO Pin
        self.STEP_Y = 14  # Step GPIO Pin
        GPIO.setup(self.DIR_MOTOR_Y, GPIO.OUT)
        GPIO.setup(self.STEP_Y, GPIO.OUT)
        print("Motors initialized.")
    
    def stop(self):
        self.keepRunning = False

    def setForce(self, forceX, forceFractionX, forceY, forceFractionY):
        self.g_forceX = forceX
        self.g_forceFractionX = forceFractionX
        self.g_forceY = forceY
        self.g_forceFractionY = forceFractionY

    #map force to steps using linear interpolation. The larger the force, the more the steps
    def calcStepCount(self, forceFraction):
        minSteps = 1
        maxSteps = 2*self.SPR_Full_Step
        return minSteps + int(round((maxSteps-minSteps)*forceFraction))

    def moveMotorX(self):
        while self.keepRunning:
            #print("In moveMotorX(), g_forceFractionX:",g_forceFractionX)
            if self.g_forceFractionX > 0.05:
                steps = self.calcStepCount(self.g_forceFractionX)
                #print("x steps:", steps)
                GPIO.output(self.DIR_MOTOR_X, self.g_forceX > 0)
                for _ in range(steps):
                    GPIO.output(self.STEP_X, GPIO.HIGH)
                    sleep(self.delay_s)
                    GPIO.output(self.STEP_X, GPIO.LOW)
                    sleep(self.delay_s)
                sleep(0.1)
        print("moveMotorX thread ended.\n")

    def moveMotorY(self):
        while self.keepRunning:
            if self.g_forceFractionY > 0.05:
                steps = self.calcStepCount(self.g_forceFractionY)
                GPIO.output(self.DIR_MOTOR_Y, self.g_forceY < 0)
                for _ in range(steps):
                    GPIO.output(self.STEP_Y, GPIO.HIGH)
                    sleep(self.delay_s)
                    GPIO.output(self.STEP_Y, GPIO.LOW)
                    sleep(self.delay_s)
                sleep(0.1)
        print("moveMotorY thread ended.\n")

    def GPIOCleanup(self):
        GPIO.cleanup() # resets any ports you have used in this program back to input mode