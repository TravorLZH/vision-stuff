import cv2
import numpy    # This seems to be useless, but it's needed to operate ndarrays
import face_recognition

# Initialize the first camera in my computer
cap=cv2.VideoCapture(0)

# mp4v: encoding for *.mp4 videos
fourcc=cv2.VideoWriter_fourcc(*'mp4v')

# Create a window to display what the camera sees
cv2.namedWindow('Camera',cv2.WINDOW_AUTOSIZE)

frames=[]

while cap.isOpened():
    ret, frame=cap.read()
    if ret==False:
        break
    frames.append(frame)
    cv2.imshow('Camera',frame)
    # Wait for 50ms (1 second / 20 fps, and stop recording if `q' is pressed
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# Destroy the camera object
cap.release()
cv2.destroyAllWindows()

# This process helps find *all* location of the faces in each of frame, but it
# takes too much time
frames_faces=face_recognition.batch_face_locations(frames,
        number_of_times_to_upsample=0)

# You can change the path if you'd like to
# 20 stands for 20 fps
# (1280,720) stands for a resolution of 1280x720
out=cv2.VideoWriter('/Users/travorlzh/Documents/capture.mp4',fourcc,20,
        (1280,720))

# This is to mark the faces for each frame using rectangles
for i, faces in enumerate(frames_faces):
    for face in faces:
        top,right,bottom,left=face
        # (0,255,0): #00FF00, or light green color
        # 3 pixels thick
        frames[i]=cv2.rectangle(frames[i],(left,top),(right,bottom),(0,255,0),3)


for frame in frames:
    out.write(frame)

out.release()

