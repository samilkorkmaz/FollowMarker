#Move marker towards marker center with stepper motors
from videoUtils import CaptureVideo
from control import generateCommands, Kp
#import firstOrderSystem
import zeroOrderSystem
from motor import moveMotorX, moveMotorY, setForce, GPIOCleanup
import threading
import time
import numpy as np
import cv2
import cv2.aruco as aruco
import markerUtil
import threading

captureVideo = CaptureVideo()

width  = captureVideo.cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
height = captureVideo.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
centerX = width/2
centerY = height/2
cameraCenterX = centerX
cameraCenterY = centerY

print("width: ", width, ", height: ", height)
radius = 41 #must be an odd number, or else GaussianBlur will fail
circleColor = (0, 0, 255) #BGR
circleThickness = 15

threading.Thread(target = captureVideo.get_frame, args = []).start()
threading.Thread(target = moveMotorX, args = []).start()
threading.Thread(target = moveMotorY, args = []).start()

time.sleep(2) #wait for camera frame to stabilize (initial frame is black)
try:
    while True:    
        image = captureVideo.frame.copy()
        [arucoMarkerDetected, xArucoMarkerCenter, yArucoMarkerCenter] = markerUtil.findArucoMarker(image)
        if arucoMarkerDetected:
            #Move marker towards brightness circle center. The marker is modelled as a first order system with PI control
            [forceX, forceY, errorStr] = generateCommands([xArucoMarkerCenter, yArucoMarkerCenter], [cameraCenterX, cameraCenterY], captureVideo.timeStep_s)
            
            #[cameraCenterX, cameraCenterY] = firstOrderSystem.#calcState([forceX, forceY], [cameraCenterX, cameraCenterY], captureVideo.timeStep_s)
            [cameraCenterX, cameraCenterY] = zeroOrderSystem.calcState([xArucoMarkerCenter, yArucoMarkerCenter], [cameraCenterX, cameraCenterY], captureVideo.timeStep_s)
            
            minForceX = 0
            maxForceX = Kp*width/2
            minForceY = 0
            maxForceY = Kp*height/2
            forceXMag = abs(forceX)
            forceYMag = abs(forceY)
            forceXMag_clipped = np.clip(forceXMag, minForceX, maxForceX)
            forceYMag_clipped = np.clip(forceYMag, minForceY, maxForceY)
            forceFractionX = (forceXMag_clipped - minForceX) / (maxForceX - minForceX)
            forceFractionY = (forceYMag_clipped - minForceY) / (maxForceY - minForceY)
            #DEBUG
            minSteps = 1
            maxSteps = 2*200
            stepsX = minSteps + round((maxSteps-minSteps)*forceFractionX)
            print("forceX:",forceX, "forceFractionX:",forceFractionX, "stepsX:", stepsX)
            #\DEBUG
            setForce(forceX, forceFractionX, forceY, forceFractionY)
            
            image = captureVideo.frame.copy()
            image = cv2.putText(image, errorStr, (0,100), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA) 
            cv2.circle(image, (xArucoMarkerCenter, yArucoMarkerCenter), radius, circleColor, circleThickness)
        # display the results of our newly improved method
        cv2.drawMarker(image, (int(cameraCenterX), int(cameraCenterY)), (255,0,0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=4, line_type=cv2.LINE_AA)
        cv2.imshow("Robust", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print('CTRL+C pressed.')        
finally:
    captureVideo.run = False #stop video capture thread
    #GPIOCleanup()
    cv2.destroyAllWindows()
    print("Main thread ended.")