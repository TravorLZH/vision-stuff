#!/usr/bin/env python3
import sys

argc=len(sys.argv)
if argc<2:
    print("usage: %s image_file" % sys.argv[0])
    exit(1)

import os
if os.path.exists(sys.argv[1])==False:
    print("%s does not exist" % sys.argv[1])
    exit(-1)

out_name="%s_inverted.png" % os.path.splitext(sys.argv[1])[0]

import cv2
import numpy as np

img=cv2.imread(sys.argv[1],cv2.IMREAD_COLOR)
img2=np.zeros_like(img)

for i,row in enumerate(img):
    for j,col in enumerate(row):
        img2[i,j]=0xFF-col

cv2.imwrite(out_name,img2)
