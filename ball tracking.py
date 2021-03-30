import numpy as np
import cv2
import distanceSensorFinal as distance
import MailingProgram as mail
from RPi.GPIO import cleanup
import time
ballLower = (88, 76, 40)
ballUpper = (129, 158, 102)
camera = cv2.VideoCapture(0)
iterator = 0
xCoordinates = []
yCoordinates = []
iterator2 = 1
iterator3 = 1
hasNotified = False
try:
    time.sleep(3)
    while True:
        if hasNotified == True:
            break
        (grabbed, frame) = camera.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, ballLower, ballUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None	
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0), 2)
                xCoordinates.append(int(x))
                yCoordinates.append(int(y))
                if iterator >= 1:
                    iterator2 = 1
                    iterator3 = 1
                    while iterator2 <= iterator:
                        while iterator3 <= iterator2:
                            cv2.line(frame,(xCoordinates[iterator-iterator2], yCoordinates[iterator-iterator2]), (xCoordinates[iterator-iterator2-1], yCoordinates[iterator-iterator2-1]), (0, 0, 255), 3)
                            iterator3 = iterator3 + 1
                        iterator2 = iterator2 + 1
            else:
                while(distance.getDistance < 1000):
                    print('Still Found')
                print('Not Found')
                if(distance.getDistance > 1000):
                    if(hasNotified == False):
                        mail.message('Object has been stolen!')
                        hasNotified = True
        cv2.imshow("Ballfinder", frame)
        key = cv2.waitKey(1) & 0xFF
        iterator = iterator + 1
        if iterator == 50:
            iterator = 0
            del xCoordinates[0:47]
            del yCoordinates[0:47]
            xCoordinates.append(int(x))
            yCoordinates.append(int(y))
        if key == ord("q"):
            break
    while True:
        distance.buzzer()
    camera.release()
    cv2.destroyAllWindows()
except Exception as e:
    camera.release()
    print(str(e))
    cv2.destroyAllWindows()
    while(distance.getDistance < 1000):
        print('Still Found')
    mail.message('An error has occoured')
    cleanup()
