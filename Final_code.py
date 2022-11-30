import cv2 as cv
import numpy as np
import sys

args = sys.argv[1:]
target_v_dir = sys.argv[1]
back_v_dir = sys.argv[2]
output_v = sys.argv[3]

width , height = 1920, 1080
video = cv.VideoCapture(target_v_dir)
backv = cv.VideoCapture(back_v_dir)
fps = video.get(cv.CAP_PROP_FPS)
recorder = cv.VideoWriter(output_v,
                                cv.VideoWriter_fourcc(*'MP4V'),
                                fps,
                                (width,height)) 

while(1):
    # Take each frame
    load_video, frames = video.read()
    load_back, b_frames = backv.read()

    frames = cv.resize(frames, (1920, 1080)) 
    b_frames = cv.resize(b_frames, (1920, 1080)) 
    # Convert BGR to HSV
    hsv = cv.cvtColor(frames, cv.COLOR_BGR2HSV)

    # define range of green color in HSV
    lower_green = np.array([36, 50, 64])
    upper_green = np.array([89, 255, 255])
    # [89, 255, 255], [36, 50, 70]
    mask = cv.inRange(hsv, lower_green, upper_green)
    
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frames,frames, mask= mask)
    f = frames - res
    f = np.where(f == 0, b_frames, f)
    
    cv.imshow('Chromakey_result',f)
    recorder.write(f)
    
    if not load_video: #video나 back 영상이 끝나면 break
        break                       
    
    if backv.get(cv.CAP_PROP_POS_FRAMES) == backv.get(cv.CAP_PROP_FRAME_COUNT):
        backv.set(cv.CAP_PROP_POS_FRAMES,0)

    if cv.waitKey(1) == 27:
        break
    
video.release()
backv.release()
recorder.release()
cv.destroyAllWindows()