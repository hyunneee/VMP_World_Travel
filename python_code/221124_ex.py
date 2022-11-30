import cv2 as cv
import numpy as np
import copy

width , height = 1920, 1080
video = cv.VideoCapture('/assets/case3/case3_fishes.mp4')
backv = cv.VideoCapture('/assets/sky.mp4')
recorder = cv.VideoWriter("recorder.mp4",
                                cv.VideoWriter_fourcc(*'MP4V'),
                                30,
                                (width,height)) 
while(1):
    # Take each frame
    load_video, frames = video.read()
    load_back, b_frames = backv.read()
    frames = cv.resize(frames, (1920, 1080)) 
    b_frames = cv.resize(b_frames, (1920, 1080)) 
    # Convert BGR to HSV
    hsv = cv.cvtColor(frames, cv.COLOR_BGR2HSV)
    
    # define range of blue color in HSV
    lower_green = np.array([50, 100, 100]) # hue(0-179), saturation(0-255), value(0-255)
    upper_green = np.array([70, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_green, upper_green)
    mask_v1 = cv.inRange(hsv, lower_green, upper_green)
    # version 1: Use cv2.copyTo()
    frames_v1 = copy.deepcopy(frames)
    b_frames_v1 = copy.deepcopy(b_frames)
    cv.copyTo(b_frames_v1,mask_v1,frames_v1)
    
    cv.imshow('chromakey',frames_v1)
    recorder.write(frames_v1)
    if not load_video or not load_back:
        break                               #video나 back 영상이 끝나면 break
    if cv.waitKey(1) == 27:
        break
backv.release()
video.release()
recorder.release()
cv.destroyAllWindows()
