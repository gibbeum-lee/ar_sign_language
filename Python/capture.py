# [GCT700] AR Project / Team 3
# OpenCV WebCam capture

import cv2
import numpy as np
from timer import Timer
import torch

MODEL_FILE = "slrecog.onnx"

win_width = 1024
win_height = 768
fps = 30
key_delay = 33 # ms

def video_start (device = 0, win_resolution = (win_width, win_height), fps = fps):
    # device = 0: system default camera, or input a video file path
    
    # Open WebCam
    try:
        capture = cv2.VideoCapture(device) # ! wsl1 or 2 cannot use camera driver ... ㅠㅠ
    except:
        print("No Camera Source Found")

    if not capture.isOpened():
        print("No Camera Opened...")
    else:
        # subwindow settings
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, win_width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, win_height)
        capture.set(cv2.CAP_PROP_FPS, fps)
        print("Camera Opened and Initialized")

    return capture

def video_capture ():
    timer = Timer()

    # Start camera
    stream = video_start()

    # Use WebCam Frames
    while stream.isOpened():

        while cv2.waitKey(key_delay) < 0:
            # capture frames from the camera
            retval, frame = stream.read() # frame is numpy.ndarray format
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
    stream.release()
    cv2.destroyAllWindows()

video_capture()