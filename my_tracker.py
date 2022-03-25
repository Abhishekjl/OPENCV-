from tracker import EuclideanDistTracker
import cv2
import numpy as np
cap  = cv2.VideoCapture('highway.mp4')
ret, frame1 = cap.read()
ret, frame2 = cap.read()

tracker = EuclideanDistTracker()


while cap.isOpened():
    # ret, frame = cap.read()
    diff = cv2.absdiff(frame1, frame2)  # this method is used to find the difference bw two  frames
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0 )
    # here i would add the region of interest to count the single lane cars 
    height, width = blur.shape
    print(height, width)
    

    # thresh_value = cv2.getTrackbarPos('thresh', 'trackbar')
    _, threshold = cv2.threshold(blur, 23, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, (1,1), iterations=1)
    contours, _, = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    detections = []
    # DRAWING RECTANGLE BOXED
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) <300:
            continue
        detections.append([x,y,w,h])

        # cv2.rectangle(frame1, (x,y),(x+w, y+h), (0,255,0), 2)
        # cv2.putText(frame1, 'status: movement',(10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    
    # cv2.drawContours(frame1,contours, -1, (0,255,0), 2)
    # cv2.imshow('frame',frame1)
    # object tracking 
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x,y,w,h,id = box_id
        cv2.putText(frame1, str(id),(x,y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.rectangle(frame1, (x,y),(x+w, y+h), (0,255,0), 2)
        cv2.imshow('frame',frame1)


    frame1 = frame2
    ret, frame2 = cap.read()

    # cv2.imshow('inter',dilated)
    # cv2.imshow('blur', blur)
    # cv2.imshow('threshold', threshold)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    key = cv2.waitKey(30)
    if key == ord('q'):
        break
cv2.destroyAllWindows()
