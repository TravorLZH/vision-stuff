#!/usr/bin/env python3
import sys
import cv2
import numpy as np

argc=len(sys.argv)

if argc<2:
    print("No files given, using webcam instead")
    video=cv2.VideoCapture(0)
else:
    video=cv2.VideoCapture(sys.argv[1])
# Use KCF to track objects
tracker=cv2.TrackerCSRT_create()


# Used by mouse_handler() and tracking
flag=False
drawing=False

# Stores current frame
frame=None

# Stores the coordinates of the rectangle
box=None
x0=0
y0=0

win="Track this"

cv2.namedWindow(win)

while video.isOpened():
    ret,frame=video.read()
    if ret==False:
        break
    if argc<2:
        frame=cv2.flip(frame,1)
    if box!=None:
        ret,newbox=tracker.update(frame)
        if ret:
            (x,y,w,h)=[int(v) for v in newbox]
            cv2.rectangle(frame,(x,y),(x+w,y+w),(0,0xFF,0),3)
    cv2.imshow(win,frame)
    key=cv2.waitKey(1) & 0xFF
    if key==ord('q'):
        break
    elif key==ord('k'):
        box=cv2.selectROI(win,frame,fromCenter=False,showCrosshair=False)
        tracker.init(np.array(frame,copy=True),box)

video.release()

cv2.destroyAllWindows()
