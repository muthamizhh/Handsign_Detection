# from matplotlib import pyplot as plt
# import matplotlib.image as mpimg
#
# img=mpimg.imread("/Users/muthamizh/PycharmProjects/HandsignDetection/Data/A/Image_1689090790.466345.jpg")
# plt.imshow(img)
# plt.show()
# import sys # to access the system
# import cv2
# # img = cv2.imread("/Users/muthamizh/PycharmProjects/HandsignDetection/Data/C/messi.jpeg", cv2.IMREAD_ANYCOLOR)
# img = cv2.imread("/Users/muthamizh/PycharmProjects/HandsignDetection/Data/D/photo-1533450718592-29d45635f0a9.jpeg", cv2.IMREAD_ANYCOLOR)
# new_width = img.shape[1] * 2# Increase width by a factor of 2
# new_height = img.shape[0] * 2# Increase height by a factor of 2
#
# # Resize the image
# resized_img = cv2.resize(img, (new_width, new_height))
# while True:
#     cv2.imshow("Sheep", img)
#     cv2.waitKey(0)
#     sys.exit() # to exit from all the processes
#
# cv2.destroyAllWindows()

import time

import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
from gtts import gTTS
from playsound import playsound

speech=["a"]
font_scale=0.5
frame_width=500
cap = cv2.VideoCapture(0)
font=cv2.FONT_HERSHEY_SIMPLEX
font_thickness=1
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

folder = "Data/C"
counter = 0

labels = ["A", "B", "C"]

welcome="Hi Guys, What do you prefer for lunch veg or non veg \n 1. Non Veg 2.Veg"
veg="you have chosen vegetarian"
non_veg="you have chosen non_vegetarian"
hello="hello all"
tags=[hello, welcome,veg,non_veg]

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    cv2.putText(imgOutput,tags[0], (50,50),cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2,cv2.LINE_AA)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgWhited = np.ones((500, 500, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
        cv2.putText(imgOutput,tags[1], (50,50),cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2,cv2.LINE_AA)
        if(labels[index]=="A"):
            tags[3]=non_veg

            # labels[index]="b"
        (text_width, text_height), _ = cv2.getTextSize(tags[3], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        if text_width > frame_width:
            font_scale *= frame_width / text_width
            (text_width, text_height), _ = cv2.getTextSize(tags[3], font, font_scale, font_thickness)


        cv2.putText(imgWhited,tags[3], (50,50),cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                      (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)

        if(speech[-1] != labels[index]):
            speech.append(labels[index])


        cv2.rectangle(imgOutput, (x-offset, y-offset),
                      (x + w+offset, y + h+offset), (255, 0, 255), 4)


        # cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhited)

    cv2.imshow("Image", imgOutput)

    key=cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Hello world")
speech.pop(0)
print(speech)
sentence =""
for i in speech:
    sentence+=i
text_val=sentence
language='en'
obj=gTTS(text=text_val, lang=language)
obj.save('sound.mp3')
playsound('sound.mp3')
