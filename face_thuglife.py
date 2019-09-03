#!/usr/bin/env python3
import numpy as np
import face_recognition as fr
from os.path import exists,splitext
import sys
import cv2

thuglife_file="./thuglife_resized.png"
assert(exists(thuglife_file))
# The second argument cv2.IMREAD_UNCHANGED is extremely important because it
# supports reading pictures using alpha channel
thuglife=cv2.imread("thuglife_resized.png",cv2.IMREAD_UNCHANGED)

assert(thuglife.shape[2]==4)    # Must have alpha channel

# determines whether to print debug messages in the session or not
debug=False

k=2

def put_sunglasses(frame,pic,mid,angle):
    h,w=pic.shape[0:2]
    coeff=0.63
    y=int(mid[1]-h/2)
    x=int(mid[0]-coeff*w)
    M=cv2.getRotationMatrix2D((w/2,h/2),angle,1)
    pic=cv2.warpAffine(pic,M,(w,h))
    a,b=y+h,x+w
    roi=frame[y:a,x:b]
    for i,row in enumerate(pic):
        for j,pix in enumerate(row):
            try:
                alpha=pix[3]
                if alpha>=0x80:
                    roi[i][j]=pix[0:3]
            except IndexError:
                continue
    frame[y:a,x:b]=roi
    return frame

def mark_eye(frame):
    small=cv2.resize(frame,(0,0),fx=1/k,fy=1/k)
    rgb_frame=small[:,:,::-1]
    all_landmarks=fr.face_landmarks(rgb_frame)
    if len(all_landmarks)==0:
        if argc>=2:
            print("Found no faces, quitting...")
            exit(1)
        return frame
    slopes=[]
    mids=[]
    for i,landmarks in enumerate(all_landmarks):
        pt1=np.array(landmarks["left_eye"][0],dtype=np.int32)
        pt2=np.array(landmarks["right_eye"][3],dtype=np.int32)
        mids.append(np.array(k*(pt1+pt2)/2,dtype=np.int32))
        diff=pt2-pt1
        width=int(k*np.sqrt(np.sum(np.square(diff))))
        ratio=width/thuglife.shape[1]*2
        slopes.append(diff[1]/diff[0])
        #frame=cv2.line(frame,(pt1[0]*k,pt1[1]*k),(pt2[0]*k,pt2[1]*k),
        #        (0xFF,0,0),2,8)
        #frame=cv2.rectangle(frame,(pt1[0]*k,pt1[1]*k),(pt2[0]*k,pt2[1]*k),
        #        (0,0xFF,0),2)
        pic=cv2.resize(thuglife,(0,0),fx=ratio,fy=ratio)
        frame=put_sunglasses(frame,pic,mids[i],-np.arctan(slopes[i])/np.pi*180)
    if debug and len(slopes)>0:
        print("Slopes: {}".format(slopes))
        print("Angles: {}".format(-np.arctan(slopes)/np.pi*180))
        print("Midpoints: {}".format([m.tolist() for m in mids]))
    return frame

def decor_img(name):
    img=cv2.imread(name)
    img=mark_eye(img)
    out="%s_thuglife.png" % splitext(name)[0]
    print("Saved to %s" % out)
    cv2.imwrite(out,img)

argc=len(sys.argv)
if argc>=2:
    k=1
    if not exists(sys.argv[1]):
        print("%s: No such file or directory" % sys.argv[1])
        exit(-1)
    decor_img(sys.argv[1])
    exit(0)

webcam=cv2.VideoCapture(0)

while webcam.isOpened():
    ret,frame=webcam.read()
    if ret==False:
        break
    frame=cv2.flip(frame,1)
    frame=mark_eye(frame)
    cv2.imshow("Thug Life",frame)
    key=cv2.waitKey(1) & 0xFF
    if key==ord('q'):
        break
    elif key==ord('k'):
        cv2.imwrite("sunglass_screenshot.png",frame)
        print("Saved")
