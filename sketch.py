#!/usr/bin/env python3

# Default high contrast level
level=5

if __name__=="__main__":
    import sys

    argc=len(sys.argv)
    if argc<2:
        print("usage: %s image_file" % sys.argv[0])
        exit(1)

    import os

    if os.path.exists(sys.argv[1])==False:
        print("%s does not exist" % sys.argv[1])
        exit(-1)

    out_name="%s_sketch.png" % os.path.splitext(sys.argv[1])[0]

import numpy as np
import cv2

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

# This function helps make higher contrast of colors
# NOTE: The variable x must be normalized previously!
def f(x):
    return 1/(1+np.exp(-level*(x-0.5)))

def make_sketch(img):
    result_x=cv2.filter2D(img,-1,sobel_x)
    result=cv2.filter2D(img,-1,sobel_y)
    result+=result_x
    # Now invert the image
    proceeded=np.zeros_like(result)
    for i,row in enumerate(result):
        for j,col in enumerate(row):
            normalized=(0xFF-col)/0xFF
            proceeded[i][j]=int(f(normalized)*0xFF)
    return proceeded

if __name__=="__main__":
    img=cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)
    final=make_sketch(img)
    # Now save the output
    cv2.imwrite(out_name,final)
