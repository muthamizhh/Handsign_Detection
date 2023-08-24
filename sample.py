import os
import pickle
import numpy as np
import cv2
# import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("/Users/muthamizh/PycharmProjects/FacialRecognition/serviceAccountsKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendencerealtime-f8911-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendencerealtime-f8911.appspot.com"
})
bucket=storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4, 480)
folderModePath='Resources/Modes'
modePathList=os.listdir(folderModePath)
imageModeList=[]
for path in modePathList:
 imageModeList.append(cv2.imread(os.path.join(folderModePath,path))) #adding all the image path to the list

imgBackround=cv2.imread('/Users/muthamizh/PycharmProjects/FacialRecognition/Resources/background.png')

#Loading the encoded file

file=open("/Users/muthamizh/PycharmProjects/FacialRecognition/venv/EncodeFile.p","rb")
encodeListKnownWithIds=pickle.load(file)
encodeListKnow , studentIds=encodeListKnownWithIds
file.close()
print(studentIds)

modeType=0
counter=0
id=0
imgStudent=[]

while True:
     success, img= cap.read()
     imgS = cv2.resize(img, (0,0),None, 0.25, 0.25)
     imgS=cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

     faceCurrentFrame= face_recognition.face_locations(imgS)
     encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)


     imgBackround[162:162+480,55:55+640]=img
     imgBackround[44:44+633,808:808+414]=imageModeList[modeType]
     if faceCurrentFrame:
         for encodeFace , faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):

             matches = face_recognition.compare_faces(encodeListKnow,encodeFace)
             faceDis = face_recognition.face_distance(encodeListKnow,encodeFace)
             # print("Matches: ", matches)
             # print("FaceDistance: ",faceDis) #lower the face distance greater the match
             matchIndex= np.argmin(faceDis)
             if matches[matchIndex]:
                  # print("Known face was detected")
                  # print(studentIds[matchIndex])
                  id=studentIds[matchIndex]
                  y1,x2,y2,x1 = faceLoc
                  y1,x2,y2,x1 =  y1*4,x2*4,y2*4,x1*4
                  bbox= 55+x1 , 162+y1,x2-x1, y2-y1
                  imgBackround=cvzone.cornerRect(imgBackround,bbox,rt=0)
                  if counter == 0:
                      cvzone.putTextRect(imgBackround,"Loading",(275,400))
                      cv2.imshow("Face Attendence",imgBackround)
                      cv2.waitKey(1)
                      counter = 1
                      modeType=1

             if counter!=0:
                 if counter==1:
                     #getting the data from the database
                     studentsInfo=db.reference(f'Students/{id}').get()
                     print(studentsInfo)


                     #getting the image
                     blob=bucket.get_blob(f'/Users/muthamizh/PycharmProjects/FacialRecognition/Images/{id}.png')
                     array=np.frombuffer(blob.download_as_string(),np.uint8)
                     imgStudent= cv2.imdecode(array, cv2.COLOR_BGRA2RGB)

                     #update data of the attendence
                     datetimeObject= datetime.strptime(studentsInfo['last_attendence_time'],
                                                      "%Y-%m-%d %H:%M:%S")
                     secondsElasped= (datetime.now()-datetimeObject).total_seconds()
                     print(secondsElasped)
                     if(secondsElasped>30):
                         ref= db.reference(f'Students/{id}')
                         studentsInfo['total_attendence']+=1
                         ref.child('total_attendence').set(studentsInfo['total_attendence'])
                         ref.child('last_attendence_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                     else:
                         modeType=0
                         counter=0
                         imgBackround[44:44+633,808:808+414]=imageModeList[modeType]



                 if modeType!=0:
                     if 10<counter<20:
                          modeType=2
                          imgBackround[44:44+633,808:808+414]=imageModeList[modeType]

                     if counter<=10:
                         cv2.putText(imgBackround,str(studentsInfo['total_attendence']),(861,125),
                                      cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
                         cv2.putText(imgBackround,str(id),(1006,493),
                                      cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)

                         cv2.putText(imgBackround,str(studentsInfo['major']),(1006,550),
                                      cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
                         cv2.putText(imgBackround,str(studentsInfo['standing']),(910,625),
                                      cv2.FONT_HERSHEY_SIMPLEX,0.6,(100,100,100),1)
                         cv2.putText(imgBackround,str(studentsInfo['year']),(1025,625),
                                      cv2.FONT_HERSHEY_SIMPLEX,0.6,(100,100,100),1)
                         cv2.putText(imgBackround,str(studentsInfo['starting_year']),(1125,625),
                                      cv2.FONT_HERSHEY_SIMPLEX,0.6,(100,100,100),1)
                         (w,h),_=cv2.getTextSize(studentsInfo['name'],cv2.FONT_HERSHEY_SIMPLEX,1,1)
                         offset=(414-w)//2
                         cv2.putText(imgBackround,str(studentsInfo['name']),(808+offset,445),
                                      cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,50),1)

                         imgBackround[175:175+216,909:909+216]=imgStudent
                     counter+=1
                     if counter>=20:
                         counter=0
                         modeType=3
                         imgStudent=[]
                         studentsInfo=[]
                         imgBackround[44:44+633,808:808+414]=imageModeList[modeType]
     else:
         modeType=3
         counter=0

     # cv2.imshow("Webcam",img)
     cv2.imshow("Face Attendence",imgBackround)
     cv2.waitKey(1)



