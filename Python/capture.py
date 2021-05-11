# [GCT700] AR Project / Team 3
# OpenCV WebCam capture

import cv2
import numpy as np
import torch

MODEL_FILE = "slrecog.onnx"

win_width = 1024
win_height = 768
key_delay = 33 # ms

# Open WebCam
try:
    camindex = 0 # 0: system default camera, or input a video file path
    capture = cv2.VideoCapture(camindex) # ! wsl1 or 2 cannot use camera driver ... ㅠㅠ
except:
    print("No Camera Source Found")

# Use WebCam Frames
while capture.isOpened():
    print("Camera Opened")

    # subwindow settings
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, win_width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, win_height)

    while cv2.waitKey(key_delay) < 0:
        # capture frames from the camera
        retval, frame = capture.read() # frame is numpy.ndarray format
        if not retval:
            break # when it failed to get a new frame

        # show frames on the subwindow
        cv2.imshow(winname = "WebCam", mat = frame)
        print(frame)

        # ====================== USING THE MODEL ==========================
        # model input here



        # model prediction here
        #net = cv2.dnn.readNet(MODEL_FILE)



        # model output here like text
        word = '테스트'



        # =================================================================

# Exit
print("Camera Closed")
capture.release()
cv2.destroyAllWindows()