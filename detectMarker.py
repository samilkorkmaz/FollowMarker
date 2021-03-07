#https://www.youtube.com/watch?v=v5a7pKSOJd8
import cv2
import cv2.aruco as aruco

def findMarker(img, markerSize=6, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    if len(bboxs) > 0:
        xSum = 0
        ySum = 0
        for i in range(4):
            xSum += bboxs[0][0][i][0]
            ySum += bboxs[0][0][i][1]
        xCenter = xSum/4
        yCenter = ySum/4
        print(bboxs[0][0])
        print("xCenter:",xCenter,", yCenter:", yCenter)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)

cap = cv2.VideoCapture(0)
try:
    while True:
        _, img = cap.read()
        findMarker(img, draw=True)
        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print('CTRL+C pressed.')        
finally:    
    cv2.destroyAllWindows()
    print("Main thread ended.")
