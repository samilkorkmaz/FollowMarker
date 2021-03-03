import numpy as np
import cv2

class CaptureVideo:
    def __init__(self):
        self.run = True        
        self.cap = cv2.VideoCapture(0)
        _, self.frame = self.cap.read() #init frame
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        #self.timeStep_s = 1/self.fps
        self.timeStep_s = 1/30.0
        print("FPS: ", self.fps, "dt: ", self.timeStep_s)

    def get_frame(self):
        while self.run:
            _, self.frame = self.cap.read()
        print("CaptureVideo.get_frame() ended.")
