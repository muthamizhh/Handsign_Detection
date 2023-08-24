import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred= credentials.Certificate("/Users/muthamizh/PycharmProjects/HandsignDetection/ServiceAccounts.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://handsigndetection-10f8f-default-rtdb.firebaseio.com/",
    "storageBucket": "handsigndetection-10f8f.appspot.com/"
})
