#!/usr/bin/env python3
import sys
import cv2
import numpy as np

argc=len(sys.argv)

if argc<2:
    print("usage: %s tracker [video_file]" % sys.argv[0])
    exit(-1)

create_tracker={
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

allowed_types=create_tracker.keys()

tracker_type=sys.argv[1]

if tracker_type not in allowed_types:
    print("error: Unknown tracker type `%s', allowed types are:\n%s"
            % (tracker_type,str.join(', ',allowed_types)))
    print("Using `csrt' as default")
    tracker_type="csrt"

if argc<3:
    print("No files given, using webcam instead")
    video=cv2.VideoCapture(0)
else:
    video=cv2.VideoCapture(sys.argv[2])

tracker=None

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
    if argc<3:
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
        tmp_box=cv2.selectROI(win,frame,fromCenter=False,showCrosshair=False)
        if tmp_box==(0,0,0,0):
            continue
        box=tmp_box
        tracker=create_tracker[tracker_type]()
        tracker.init(np.array(frame,copy=True),box)

video.release()

cv2.destroyAllWindows()
