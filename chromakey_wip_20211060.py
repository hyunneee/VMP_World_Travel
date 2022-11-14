
import cv2 as cv
import numpy as np

filename = '/Users/seohyunoh/Documents/python/VMP/chroma-key/chroma-keying.mp4'
cap = cv.VideoCapture(str(filename))
image = cv.imread("eiffel-tower.jpg")
while(1):
    # Take each frame
    _, frame = cap.read()

    frame = cv.resize(frame, (1920, 1080))
    image = cv.resize(image, (1920, 1080))
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([30, 30, 0])
    upper_blue = np.array([60, 255, 255])
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    f = frame - res
    f = np.where(f == 0, image, f)

    cv.imshow('frame',frame)
    cv.imshow('mask',f)
    # cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()