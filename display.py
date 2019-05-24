#!/usr/bin/env python3
import sys
import cv2
import numpy

assert(len(sys.argv)>=2)

# Load the image file into an ndarray
image=cv2.imread(sys.argv[1],cv2.IMREAD_UNCHANGED);

# Show it!
cv2.imshow('OpenCV\'s image viewer',image)
# Press any key to terminate
cv2.waitKey(0)
