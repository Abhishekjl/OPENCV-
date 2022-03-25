import cv2

cap = cv2.VideoCapture('highway.mp4')
from cv2 import bgsegm

# object detection from stable camera
# object_detector = cv2.createBackgroundSubtractorMOG2()

object_detector = bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame = cap.read()

    mask = object_detector.apply(frame)


    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()