#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import os

argc=len(sys.argv)
if argc<2:
    print("usage: %s image_file" % sys.argv[0])
    exit(1)

if os.path.exists(sys.argv[1])==False:
    print("%s does not exist" % sys.argv[1])
    exit(-1)

# Output file name
output_name="%s_sobel.png" % os.path.splitext(sys.argv[1])[0]

# Detect edges using sobel operator
sobel_x=np.array([
    [-1,0,1],
    [-2,0,2],
    [-1,0,1]
])

sobel_y=np.array([
    [1,2,1],
    [0,0,0],
    [-1,-2,-1]
])

img=cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)
result_x=cv2.filter2D(img,-1,sobel_x)
result_y=cv2.filter2D(img,-1,sobel_y)
result=result_x+result_y

cv2.imwrite(output_name,result)
