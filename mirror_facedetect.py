# mirror_facedetect.py: Detect faces in the view of webcam
import cv2
import numpy
import face_recognition
import sys

# Increase this number to speed up and lower the accuracy
k=4

# Allow users to change k while running
if len(sys.argv)>=2:
    k=int(sys.argv[1])

colors=[(0,0xFF,0),(0xFF,0xFF,0),(0xFF,0,0)]

def mark_faces(frm):
    smaller_frm=cv2.resize(frm,(0,0),fx=1/k,fy=1/k)   # To increase speed
    # Convert BGR (OpenCV uses) to RGB to reduce time on dealing with colors
    rgb_frm=smaller_frm[:,:,::-1]
    faces=face_recognition.face_locations(rgb_frm)
    for i,face in enumerate(faces):
        top,right,bottom,left=face
        frm=cv2.rectangle(frm,(k*left,k*top),(k*right,k*bottom),colors[i%3],3)
    return frm

camera=cv2.VideoCapture(0)

while camera.isOpened():
    ret, frm=camera.read()
    if ret==False:
        break
    frm=cv2.flip(frm,1)
    # This is just to put rectangle to highlight the faces
    mark_faces(frm)
    cv2.imshow('The Mirror',frm)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
