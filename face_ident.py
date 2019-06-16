#!/usr/bin/env python3
import cv2
import os
import numpy as np
import face_recognition as fr

encodings=[]
names=[]
k=4

imgdir="./known_people"
files=os.listdir(imgdir)

for f in files:
    parts=f.split('.')
    filename=os.path.join(imgdir,f)
    assert(len(parts)==2)   # Assume no other dots in the file
    if parts[1]=="face":    # If it's .face file, then read directly
        encoding=np.loadtxt(filename)
    else:   # If it's an image file, then generate encoding from it
        img=fr.load_image_file(filename)
        encoding=fr.face_encodings(img)[0]
    name=parts[0]
    name=name.replace('_',' ')
    print("Append `%s' to face library" % name)
    encodings.append(encoding)
    names.append(name)

vid=cv2.VideoCapture(0)

def decorate(frame):
    small=cv2.resize(frame,(0,0),fx=1.0/k,fy=1.0/k)
    rgb_frame=small[...,::-1]   # Convert it to RGB to increase efficiency
    face_pos=fr.face_locations(rgb_frame,model="cnn")
    face_codes=fr.face_encodings(rgb_frame,face_pos)
    for (top,right,bottom,left),code in zip(face_pos,face_codes):
        name="Unknown"
        faces=fr.compare_faces(encodings,code)
        distances=fr.face_distance(encodings,code)
        i=np.argmin(distances)
        if distances[i] <= 0.5 and faces[i]:
            name=names[i]
        frame=cv2.rectangle(frame,(left*k,top*k),(right*k,bottom*k),
                (0,0xFF,0),2)
        frame=cv2.putText(frame,name,(left*k+6*k,bottom*k-6*k),
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
