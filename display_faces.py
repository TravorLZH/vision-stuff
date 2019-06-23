#!/usr/bin/env python3
import sys

argc=len(sys.argv)

if argc<2:
    print("usage: %s image_file" % sys.argv[0])
    exit(-1)

import face_recognition as fr
import numpy as np
import cv2

image=fr.load_image_file(sys.argv[1])   # This is for face detection
cvimg=cv2.imread(sys.argv[1],cv2.IMREAD_UNCHANGED)
faces=fr.face_locations(image)

for top,right,bottom,left in faces:
    cvimg=cv2.rectangle(cvimg,(left,top),(right,bottom),(0,0xFF,0),3)

cv2.imshow("Results from face detector",cvimg)
cv2.waitKey(0)
