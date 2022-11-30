import cv2 as cv
import numpy as np
import copy
import sys

args = sys.argv[1:]
target_v_dir = sys.argv[1]
back_v_dir = sys.argv[2]
output_v = sys.argv[3]
for i in args:
    print(i)
width , height = 1920, 1080
video = cv.VideoCapture(target_v_dir)
backv = cv.VideoCapture(back_v_dir)
recorder = cv.VideoWriter(output_v,
                                cv.VideoWriter_fourcc(*'MP4V'),
                                29.97,
                                (width,height)) 

while(1):
    # Take each frame
    load_video, frames = video.read()
    load_back, b_frames = backv.read()
    # print(load_video, frames)
    frames = cv.resize(frames, (1920, 1080)) 
    b_frames = cv.resize(b_frames, (1920, 1080)) 
    # Convert BGR to HSV
    hsv = cv.cvtColor(frames, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_green = np.array([45, 60, 100])
    upper_green = np.array([89, 255, 255])
# [89, 255, 255], [36, 50, 70]
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_green, upper_green)
    mask_v1 = cv.inRange(hsv, lower_green, upper_green)
    # version 1: Use cv2.copyTo()
    frames_v1 = copy.deepcopy(frames)
    b_frames_v1 = copy.deepcopy(b_frames)
    cv.copyTo(b_frames_v1,mask_v1,frames_v1)
    # version 2: Bitwise-AND mask and original image
    res = cv.bitwise_and(frames,frames, mask= mask)
    f = frames - res
    f = np.where(f == 0, b_frames, f)
    # diff = (frames_v1 - f)
    # print(diff)
    cv.imshow('frame_version1',frames_v1)
    # cv.imshow('frame_version2',frames)
    # cv.imshow('mask',f)
    # cv.imshow('res',res)
    recorder.write(frames_v1)
    # if not load_back:
    #     load_back = True
    if not load_video:
        break                               #video나 back 영상이 끝나면 break
    # if not load_back:
    if backv.get(cv.CAP_PROP_POS_FRAMES) == backv.get(cv.CAP_PROP_FRAME_COUNT):
        backv.set(cv.CAP_PROP_POS_FRAMES,0)

    if cv.waitKey(1) == 27:
        break
video.release()
backv.release()
recorder.release()
cv.destroyAllWindows()