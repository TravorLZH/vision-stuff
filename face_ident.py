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
    print("Storing `%s' to face library" % name)
    encodings.append(encoding)
    names.append(name)

vid=cv2.VideoCapture(0)

def decorate(frame,rgb_frame,face_pos,face_codes):
    for i,((top,right,bottom,left),code) in enumerate(zip(face_pos,face_codes)):
        name="Unknown ID %d" % i
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
    small=cv2.resize(frame,(0,0),fx=1.0/k,fy=1.0/k)
    rgb_frame=small[...,::-1]   # Convert it to RGB to increase efficiency
    face_pos=fr.face_locations(rgb_frame,model="cnn")
    face_codes=fr.face_encodings(rgb_frame,face_pos)
    frame=decorate(frame,rgb_frame,face_pos,face_codes)
    cv2.imshow("That is you",frame)
    key=cv2.waitKey(1) & 0xFF
    if key==ord('q'):
        break
    elif key==ord('k'): # Pause
        i=int(input("Enter ID: "))
        name=input("Enter new name for ID %d: " % i)
        filename=os.path.join(imgdir,name.replace(' ',"_")+".face")
        encodings.append(face_codes[i])
        names.append(name)
        print("Storing `%s' to face library" % name)
        np.savetxt(filename,face_codes[i])

vid.release()
