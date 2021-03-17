#https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/
#Two Nema stepper motors test with Raspberry Pi
from time import sleep
import RPi.GPIO as GPIO
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

DIR_1 = 15   # Direction GPIO pin for motor 1
STEP_1 = 14  # Step GPIO pin for motor 1
GPIO.setup(DIR_1,GPIO.OUT)
GPIO.setup(STEP_1,GPIO.OUT)

DIR_2 = 20   # Direction GPIO pin for motor 2
STEP_2 = 21  # Step GPIO pin for motor 2
GPIO.setup(DIR_2, GPIO.OUT)
GPIO.setup(STEP_2, GPIO.OUT)

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR_Full_Step = 200   # Steps per revolution for Nema 17 stepper motor

step_count = SPR_Full_Step * 1
delay = 1.0 / SPR_Full_Step / 8

def runMotor1Basic():
    for _ in range(step_count):
        GPIO.output(STEP_1, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_1, GPIO.LOW)
        sleep(delay)   

def runMotor1():
    for _ in range(3):
        GPIO.output(DIR_1, CW)
        runMotor1Basic()
        sleep(1)
        GPIO.output(DIR_1, CCW)
        runMotor1Basic()
         
threading.Thread(target = runMotor1, args = []).start()

def runMotor2():
    for _ in range(step_count):
        GPIO.output(STEP_2, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_2, GPIO.LOW)
        sleep(delay)    

print("Starting two Nema motors test...")
try:
    for _ in range(3):
        GPIO.output(DIR_2, CW)
        runMotor2()
        sleep(1)
        GPIO.output(DIR_2, CCW)
        runMotor2()
            
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    print("Finished")