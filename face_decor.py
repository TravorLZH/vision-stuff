#!/usr/bin/env python3
import cv2
import numpy as np
import face_recognition as fr

webcam=cv2.VideoCapture(0)
k=2

def do_decor(frame):
    small_frame=cv2.resize(frame,(0,0),fx=1/k,fy=1/k)
    frame_rgb=small_frame[:,:,::-1]
    all_face_landmarks=fr.face_landmarks(frame_rgb)
    for face_landmarks in all_face_landmarks:
        eyebrow_l=np.array(face_landmarks["left_eyebrow"],np.int32)
        eyebrow_r=np.array(face_landmarks["right_eyebrow"],np.int32)
        nose_tip=np.array(face_landmarks["nose_tip"],np.int32)
        nose_bridge=np.array(face_landmarks["nose_bridge"],np.int32)
        nose=np.array([nose_bridge[0],nose_tip[0],nose_tip[-1]])
        top_lip=np.array(face_landmarks["top_lip"],np.int32)
        bottom_lip=np.array(face_landmarks["bottom_lip"],np.int32)
        frame=cv2.fillPoly(frame,[k*eyebrow_l,k*eyebrow_r],(0xFF,0xFF,0xFF))
        frame=cv2.fillPoly(frame,[k*nose],(0,0x80,0xFF))
        frame=cv2.fillPoly(frame,[k*bottom_lip],(0,0,0xFF))
        frame=cv2.fillPoly(frame,[k*top_lip],(0,0xFF,0))
    return frame

while webcam.isOpened():
    ret,frame=webcam.read()
    if ret==False:
        break
    frame=cv2.flip(frame,1)
    frame=do_decor(frame)
    cv2.imshow("Yourself with decorations",frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

webcam.release()
