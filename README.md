# [2022-2]VMP_TP1

## A World Travel By Chromakey

### Team member : 20211060 오서현, 20201043 김선경, 20190365 김찬주


#이미 인터넷에 코드가 정말 많은데..
#구체적인 코드와 스텝, 설명까지 나와있는 사이트가 있어 데려옵니다,, 
#https://medium.com/fnplus/blue-or-green-screen-effect-with-open-cv-chroma-keying-94d4a6ab2743
import cv2
import matplotlib.pyplot as plt
import numpy as np
image = cv2.imread(' 그린스크린 영상 경로 이름 ')

img_copy = np.copy(image)
image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGE2GRB)
plt.imshow(image_copy)

lower_blue = np.array([0, 0, 100])
upper_blue = np.array([120, 100, 255])

mask = cv2.inRange(image_copy, lower_blue, upper_blue)
plt.show(mask, cmap='gray')

masked_image = np.copy(image_copy)
masked_image[mask !=0] = [0, 0, 0]
plt.imshow(masked_image)

background_image = cv2.imread('배경 이미지, 경로')
background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)

crop_background = background_image[0:720, 0:1280]

crop_background[mask == 0] = [0, 0, 0]

plt.imshow(crop_background

final_image = crop_background + masked_image
plt.imshow(final_image)
