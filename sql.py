import mysql.connector
cnn=mysql.connector.connect(user="root",password='Jailer123',host='localhost')
if (cnn):
    print("it works")
