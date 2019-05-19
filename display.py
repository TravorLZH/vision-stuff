import sys
import cv2
import numpy

# Make sure user enters the path of image as an argument
if len(sys.argv)<2:
    print("Insufficient arguments")
    exit(1)

# Load the image file into an ndarray
image=cv2.imread(sys.argv[1],cv2.IMREAD_UNCHANGED);

# Show it!
cv2.imshow('OpenCV\'s image viewer',image)
# Press any key to terminate
cv2.waitKey(0)
