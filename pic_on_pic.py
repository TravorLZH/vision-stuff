#!/usr/bin/env python3
import cv2
import numpy as np
import face_recognition as fr

background=cv2.imread("known_people/Barack_Obama.jpg",cv2.IMREAD_COLOR)
foreground=cv2.imread("thuglife.png",cv2.IMREAD_UNCHANGED)

[face]=fr.face_locations(background[:,:,::-1])
top,right,left,bottom=face

assert(foreground.shape[2]==4)  # Assume foreground image has alpha channel

height=foreground.shape[0]
width=foreground.shape[1]

a=top
b=left

c=a+height
d=b+width

roi=background[a:c,b:d]
for i,row in enumerate(foreground):
    for j,pix in enumerate(row):
        alpha=pix[3]/0xFF
        mixed=pix[0:3]*alpha+roi[i][j]*(1-alpha).astype(np.int8)
        roi[i][j]=mixed

background[a:c,b:d]=roi

cv2.imshow("Mixed",background)
cv2.waitKey(0)
