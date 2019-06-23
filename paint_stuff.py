#!/usr/bin/env python3
import sys

argc=len(sys.argv)

if argc<2:
    print("usage: %s background_image" % sys.argv[0])
    exit(-1)

img_fname=sys.argv[1]

import cv2
import numpy as np

x0=0
y0=0
flag=False

img=cv2.imread(img_fname,cv2.IMREAD_UNCHANGED)

win="~Put some rectangles~"

def mouse_handler(event,x,y,flags,param):
    global x0,y0,flag
    if event==cv2.EVENT_LBUTTONDOWN:
        print("Start drawing")
        flag=True
        x0=x
        y0=y
    elif event==cv2.EVENT_MOUSEMOVE:
        if flag:
            tmp=np.array(img,copy=True)  # Make a copy from it
            cv2.rectangle(tmp,(x0,y0),(x,y),(0,0xFF,0),3)
            cv2.imshow(win,tmp)
    elif event==cv2.EVENT_LBUTTONUP:
        flag=False
        print("Rectangle between (%d,%d) and (%d,%d)" % (x0,y0,x,y))
        cv2.rectangle(img,(x0,y0),(x,y),(0,0xFF,0),3)
        cv2.imshow(win,img)

cv2.namedWindow(win)
cv2.setMouseCallback(win,mouse_handler)
cv2.imshow(win,img)
cv2.waitKey(0)
