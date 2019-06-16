Computer Vision Demonstration
=============================

This repo is storing my programs created during a Face Recognition course at
Institute of Automation, Chinese Academy of Sciences. To run it, you need to
have:

* A working **python3**
* Module `opencv-python`
* Module `numpy`
* Module `face_recognition`
* Module `dlib`

## Install Prerequisites

Installing those packages are not that hard, we can just puts these commands
into the terminal:
```shell
$ brew install python		# This installs Python 3.7 by HomeBrew
$ pip3 install opencv-python	# This installs numpy as its dependency
$ pip3 install face_recognition	# This installs dlib as its dependency
```

## What this repo has

* **display.py** program to show a picture using OpenCV functions
* **video\_capture.py** to record what's in the webcam
* **mirror\_facedetect.py** to detect faces in the webcam
* **face\_ident.py** to identify the actual person from their faces
