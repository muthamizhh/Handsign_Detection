import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred= credentials.Certificate("/Users/muthamizh/PycharmProjects/HandsignDetection/ServiceAccounts.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://handsigndetection-10f8f-default-rtdb.firebaseio.com/"
})

ref= db.reference("Food Items")
data ={
    "165":{
        "name":"Chicken Biriyani",
        "price":390,
        "rating":5
    },
    "166":{
        "name":"Mutton Biriyani",
        "price":490,
        "rating":4.75
    },
    "167":{
        "name":"Grilled Chicken",
        "price":390,
        "rating":4.5
    },
    "168":{
        "name":"Pepper Chicken ",
        "price":290,
        "rating":4.23
    },
    "169":{
        "name":"Chettinad Chicken ",
        "price":310,
        "rating":4.5
    },
    "170":{
        "name":"Mutton Roast",
        "price":510,
        "rating":4.9
    },
    "265":{
        "name":"Paneer Biriyani",
        "price":290,
        "rating":4.5
    },
    "266":{
        "name":"Mushroom Biriyani",
        "price":290,
        "rating":4.45
    },

    "267":{
        "name":"Grilled Paneer",
        "price":190,
        "rating":4.4
    },

    "268":{
        "name":"Pepper Mushroom ",
        "price":190,
        "rating":4.45
    },

    "269":{
        "name":"Chettinad Mushroom ",
        "price":190,
        "rating":4.45
    },
    "270":{
        "name":"Paneer Roast",
        "price":390,
        "rating":4.2
    }
}






# id=321654
for key, val in data.items():
    ref.child(key).set(val)
# studentsInfo=db.reference(f'Students/{id}').get()
# print(studentsInfo)
