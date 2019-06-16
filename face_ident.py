#!/usr/bin/env python3
import cv2
import os
import numpy as np
import face_recognition as fr

encodings=[]
names=[]

files=os.listdir("./known_people")

for f in files:
    img=fr.load_image_file(os.path.join("./known_people",f))
    encoding=fr.face_encodings(img)[0]
    name=f.split('.')[0]    # Assume no other dots in the file
    name=name.replace('_',' ')
    encodings.append(encoding)
    names.append(name)

vid=cv2.VideoCapture(0)

def decorate(frame):
    rgb_frame=frame[...,::-1]   # Convert it to RGB to increase efficiency
    face_pos=fr.face_locations(rgb_frame)
    face_codes=fr.face_encodings(rgb_frame,face_pos)
    for (top,right,bottom,left),code in zip(face_pos,face_codes):
        name="Unknown"
        faces=fr.compare_faces(encodings,code)
        distances=fr.face_distance(encodings,code)
        i=np.argmin(distances)
        if faces[i]:
            name=names[i]
        frame=cv2.rectangle(frame,(left,top),(right,bottom),(0,0xFF,0),2)
        frame=cv2.putText(frame,name,(left+24,bottom-24),
                cv2.FONT_HERSHEY_DUPLEX,1.0,(0xFF,0xFF,0xFF),1)
    return frame

while vid.isOpened():
    ret,frame=vid.read()
    if ret==False:
        break
    # Create mirror image
    frame=cv2.flip(frame,1)
    frame=decorate(frame)
    cv2.imshow("That is you",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
