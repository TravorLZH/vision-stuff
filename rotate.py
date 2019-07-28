#!/usr/bin/env python3
import sys
import cv2
import numpy as np

argc=len(sys.argv)
if argc<3:
    print("usage: %s image_file counter_clockwise" % sys.argv[0])
    exit(-1)

degree=float(sys.argv[2])
rad=degree*np.pi/180.0

image=cv2.imread(sys.argv[1],cv2.IMREAD_UNCHANGED)

height,width=image.shape[0:2]   # Get the shape

print("w=%d,h=%d" % (width,height))

M=cv2.getRotationMatrix2D((width/2,height/2),degree,1)


image=cv2.warpAffine(image,M,(width,height))

cv2.imshow("Rotated",image)
cv2.waitKey(0)
