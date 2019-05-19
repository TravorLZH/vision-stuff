import cv2
import numpy    # This seems to be useless, but it's needed to operate ndarrays

# Initialize the first camera in my computer
cap=cv2.VideoCapture(0)

# mp4v: encoding for *.mp4 videos
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
# You can change the path if you'd like to
# 20 frames per second
# (1280,720) stands for a resolution of 1280x720
out=cv2.VideoWriter('/Users/travorlzh/Documents/capture.mp4',fourcc,20.0,
        (1280,720))


# Create a window to display what the camera sees
cv2.namedWindow('Camera',cv2.WINDOW_AUTOSIZE)

while cap.isOpened():
    ret, frame=cap.read()
    if ret==False:
        break
    out.write(frame)
    cv2.imshow('Camera',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Destroy the camera object
cap.release()
cv2.destroyAllWindows()
out.release()

