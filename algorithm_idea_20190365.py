#20190365 김찬주
import cv2
import numpy as np

#영상과 사용할 배경 이미지 불러오기
video = cv2.VideoCapture('영상.mp4')
back = cv2.imread("background.jpg")   #배경이 영상일 경우: cv2.VideoCapture('배경.mp4')

#video의 기본 정보들
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
nframes = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
fourcc = int(video.get(cv2.CAP_PROP_FOURCC))
fps = video.get(cv2.CAP_PROP_FPS)
#fps_b = back.get(cv2.CAP_PROP_FPS)

print(width, height, fps, nframes, fourcc)


#한 프레임마다 적용되도록 무한 루프
while True: 
    load_video, frames = video.read()       #load_video: 영상이 load 됐으면 True
    background = back                       #배경이 영상일 경우: load_background, background = back.read()
    if background.all() == True:
        load_background = True              #load_background: 영상이 load 됐으면 True

    if not load_video or not load_background:
        break                               #video나 back 영상이 끝나면 break

    #알고리즘 아이디어
    hsv = cv2.cvtColor(frames, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (90, 150, 0), (120, 255, 255))
    cv2.copyTo(background, mask, frames)

    #showing
    cv2.imshow('chroma-key', frames)
    if cv2.waitKey(30) == 27: break