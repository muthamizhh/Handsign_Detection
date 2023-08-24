import time

import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from gtts import gTTS
from playsound import playsound

cred = credentials.Certificate("/Users/muthamizh/PycharmProjects/HandsignDetection/ServiceAccounts.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://handsigndetection-10f8f-default-rtdb.firebaseio.com/",
    # 'storageBucket': "faceattendencerealtime-f8911.appspot.com"
})

speech=["a"]
id=0
foodnv=[]
foodveg=[]
food=(cv2.imread(os.path.join("/Users/muthamizh/PycharmProjects/HandsignDetection/Resources/NV","1A.png")))
def imgselect(path, img):
    imgback = (cv2.imread(os.path.join(path,img)))
    print(imgback)
    return imgback


cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
imgBackround=cv2.imread('/Users/muthamizh/PycharmProjects/HandsignDetection/Resources/background.png')
# print(imgBackround)
offset = 20
imgSize = 300

# food=(cv2.imread("/Users/muthamizh/PycharmProjects/HandsignDetection/Resources/NV/1B.png"))
# print(food)

modeType=1
counter=0
id=0

folder = "Data/C"
# counter = 0

labels = ["1","2","A", "B", "C","D","E","F"]


folderModePath='Resources/Modes'
modePathList=os.listdir(folderModePath)
imageModeList=[]
i =0
for path in modePathList:
     imageModeList.append(cv2.imread(os.path.join(folderModePath,path))) #adding all the image path to the list
     # print(path)
     # print(imageModeList[i])
     # i+=1

vegpath='Resources/VEG'
veglist=os.listdir(vegpath)
print(veglist)

for path in veglist:

    print(path)
    foodveg.append(cv2.imread(os.path.join(vegpath,path)))


for i in range(len(foodveg)):
    print(foodveg[i])

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    imgBackround[44:44+633,808:808+414]=imageModeList[modeType+1]


    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
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
            # print(prediction, index)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                      (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        # if (labels[index]=='C'):
        #     key=cv2.waitKey(2)
        #     key = ord("q")
        #
        #
        #     if (key == ord('q')):
        #         break
        if(labels[index]=='2'):
            modeType=2
            imgBackround[44:44+633,808:808+414]=imageModeList[modeType+1]
            path="/Users/muthamizh/PycharmProjects/HandsignDetection/Resources/NV"

        if ((labels[index]=="A" or labels[index]=="C" or labels[index]=="D")  and modeType==2):
        # if (modeType==2):
            modeType=3
            id=100+ord(labels[index])
            imgfit = str(1)+labels[index]+".png"
            # print(imgfit)
            # foodimg.append(cv2.imread(os.path.join("/Users/muthamizh/PycharmProjects/HandsignDetection/Resources/NV","1A.png")))
            food=(cv2.imread(os.path.join("/Users/muthamizh/PycharmProjects/HandsignDetection/Resources/NV",imgfit)))

            # food = imgselect(path,imgfit)
            # food = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)
            # foodimg.pop(0)
            # print(foodimg)
            imgBackround[175:175+216,909:909+216]=food
            imgBackround[44:44+633,808:808+414]=imageModeList[modeType+1]



        if(labels[index]=='1'):
            modeType=0
            imgBackround[44:44+633,808:808+414]=imageModeList[modeType+1]
            # if (labels[index]=="A"):
            #     modeType=3
            #     imgBackround[44:44+633,808:808+414]=imageModeList[modeType+1]

        if(speech[-1] != labels[index]):
            speech.append(labels[index])


        cv2.rectangle(imgOutput, (x-offset, y-offset),
                      (x + w+offset, y + h+offset), (255, 0, 255), 4)


        # cv2.imshow("ImageCrop", imgCrop)
        # cv2.imshow("ImageWhite", imgWhite)

    # cv2.imshow("Image", imgOutput)

    #     foodinfo=db.reference(f'Food Items/{id}').get()
    #     print(foodinfo)

        # if (modeType==3):
        #     imgBackround[175:175+216,909:909+216]=food
        #     (w,h),_=cv2.getTextSize(foodinfo['name'],cv2.FONT_HERSHEY_SIMPLEX,1,1)
        #     offset=(414-w)//2
        #     cv2.putText(imgBackround,str(foodinfo['name']),(808+offset,445),
        #                                       cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,50),1)
    imgBackround[44:44+633,808:808+414]=imageModeList[modeType+1]
    if (modeType==3):
        imgBackround[175:175+216,909:909+216]=food
        # (w,h),_=cv2.getTextSize(foodinfo['name'],cv2.FONT_HERSHEY_SIMPLEX,1,1)
        # offset=(414-w)//2
        # cv2.putText(imgBackround,str(foodinfo['name']),(808+offset,445),
        #                                   cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,50),1)
    imgOutput=cv2.resize(imgOutput,(640,480))
    imgBackround[162:162+480,55:55+640] = imgOutput
    cv2.imshow("Food Ordering",imgBackround)

    key=cv2.waitKey(1)

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
# print("Hello world")
# speech.pop(0)
# print(speech)
# sentence =""
# for i in speech:
#     sentence+=i
# text_val=sentence
# language='en'
# obj=gTTS(text=text_val, lang=language)
# obj.save('sound.mp3')
# playsound('sound.mp3')
