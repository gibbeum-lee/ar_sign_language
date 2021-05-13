# [GCT700] AR Project / Team 3
# OpenCV WebCam capture

import cv2
import numpy as np
#import torch
import math
import socket
import time

#MODEL_FILE = "slrecog.onnx"

# WebCam Settings
win_width = 1024
win_height = 768
fps = 30
key_delay = 33 # ms

# Networking
RECEIVER_IP = 'localhost'
RECEIVER_PORT = 9999
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Socket for Sender

# Start the WebCam
def video_start (device = 0, win_resolution = (win_width, win_height), fps = fps):
    # device = 0: system default camera, or input a video file path
    
    # Open WebCam
    try:
        capture = cv2.VideoCapture(device) # ! wsl1 or 2 cannot use camera driver ... ㅠㅠ
        # VideoCapture에 RTSP 주소를 넘겨서 스트리밍을 처리할 수 있음.
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

# Streaming Analysis -> Sending message to UDP receiver
def stream_capture ():
    # Start camera
    stream = video_start()
    time_fingers = []
    
    # Use WebCam Frames
    while cv2.waitKey(key_delay) < 0:

        # capture frames from the camera
        retval, frame = stream.read() # frame is numpy.ndarray format
        if not retval:
            break # when it failed to get a new frame

        # ====================== USING TEMP DETECTION ==========================
        # Recognition box*
        cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)
        crop_image = frame[100:500, 100:500]

        # Apply Gaussian blur
        blur = cv2.GaussianBlur(crop_image, (3,3), 0)
        
        # Change color-space from BGR -> HSV
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        
        # Create a binary image with where white will be skin colors and rest is black
        mask2 = cv2.inRange(hsv, np.array([2,0,0]), np.array([20,255,255]))
        
        # Kernel for morphological transformation    
        kernel = np.ones((5,5))
        
        # Apply morphological transformations to filter out the background noise
        dilation = cv2.dilate(mask2, kernel, iterations = 1)
        erosion = cv2.erode(dilation, kernel, iterations = 1)    
        
        # Apply Gaussian Blur and Threshold
        filtered = cv2.GaussianBlur(erosion, (3,3), 0)
        ret,thresh = cv2.threshold(filtered, 127, 255, 0)
        
        # Show threshold image
        cv2.imshow("Thresholded", thresh)

        # Find contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        # Find contour with maximum area
        contour = max(contours, key = lambda x: cv2.contourArea(x))
        
        # Create bounding rectangle around the contour
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(crop_image,(x,y),(x+w,y+h),(0,0,255),0)
        
        # Find convex hull
        hull = cv2.convexHull(contour)
        
        # Draw contour
        drawing = np.zeros(crop_image.shape, np.uint8)
        cv2.drawContours(drawing,[contour],-1,(0,255,0),0)
        cv2.drawContours(drawing,[hull],-1,(0,0,255),0)
        
        # Find convexity defects
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour,hull)
        
        # Use cosine rule to find angle of the far point from the start and end point i.e. the convex points (the finger 
        # tips) for all defects
        count_defects = 0
        
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])

            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = (math.acos((b**2 + c**2 - a**2)/(2*b*c))*180)/3.14
            
            # if angle > 90 draw a circle at the far point
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_image,far,1,[0,0,255],-1)

            cv2.line(crop_image,start,end,[0,255,0],2)

        # Print number of fingers
        print("Defects : ", count_defects)
        if count_defects == 0:
            cv2.putText(frame,"ZERO", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 1:
            cv2.putText(frame,"TWO", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 2:
            cv2.putText(frame, "THREE", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 3:
            cv2.putText(frame,"FOUR", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
            cv2.putText(frame,"FIVE", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        else:
            pass

        # Show required images
        cv2.imshow("Full Frame", frame)
        all_image = np.hstack((drawing, crop_image))
        cv2.imshow('Recognition', all_image)

        time_fingers.append(count_defects)
        if(len(time_fingers) > 5):
            time_fingers = time_fingers[-5:]
        print(time_fingers)

        # Check if previously hand was wide open (3/4 fingers in previous frames), and is now a fist (0 fingers)
        if(count_defects == 0 and 4 in time_fingers):
            time_fingers = []
            msg = "안녕하세요"
            msg = bytes(msg.encode())
            socket.sendto(msg, (RECEIVER_IP, RECEIVER_PORT))
            print("_" * 10, "Sign Language Triggered!", "_" * 10)

        # ====================== USING THE MODEL ==========================
        # model input here
        print(frame) # pixels per frame



        # model prediction here
        #net = cv2.dnn.readNet(MODEL_FILE)



        # model output here like text
        word = '테스트'



        # =================================================================

    # Exit
    print("Camera Closed")
    stream.release()
    cv2.destroyAllWindows()
    socket.close()

stream_capture()