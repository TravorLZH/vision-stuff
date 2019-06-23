#!/usr/bin/env python3
import sys

argc=len(sys.argv)

if argc<2:
    print("usage: %s image_file" % sys.argv[0])
    exit(-1)

import cv2
import numpy

# Load the image file into an ndarray
image=cv2.imread(sys.argv[1],cv2.IMREAD_UNCHANGED);

# Show it!
cv2.imshow('OpenCV\'s image viewer',image)
# Press any key to terminate
cv2.waitKey(0)
