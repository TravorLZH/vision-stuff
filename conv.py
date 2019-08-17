#!/usr/bin/env python3
import cv2
import numpy as np

img=cv2.imread("lena.png",cv2.IMREAD_COLOR)
kernel=np.array([
    [-1,0,1],
    [-2,0,2],
    [-1,0,1]
],np.float32)
print(kernel)
result=cv2.filter2D(img,-1,kernel)
merged=np.hstack([img,result])
cv2.imshow("Lena",merged)
cv2.waitKey(0)
