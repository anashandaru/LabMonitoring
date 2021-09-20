import pyrebase
from datetime import datetime
from config import firebaseConfig, labName
from Database import ReadFromDB

def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

# config ={
#     "apiKey":"AIzaSyCsSxN_pAQbl_ePNSyRY8oJhx_mtvTAA3o",
#     "authDomain": "labmon-5dd47.firebaseapp.com",
#     "databaseURL":"https://labmon-5dd47-default-rtdb.asia-southeast1.firebasedatabase.app/",
#     "storageBucket": "labmon-5dd47.appspot.com"
# }

def upload(humi, temp, timestamp, lab=labName):
    fb = pyrebase.initialize_app(firebaseConfig)
    db = fb.database()
    data = {'lab':lab,
            'humi':humi,
            'temp':temp,
            'timestamp':timestamp
            }
    reply = db.child('measurements').push(data)
    return reply

def backup():
    records = ReadFromDB()
    count = 0
    for item in records:
        timestamp = datetime.timestamp(item[0])*1000
        upload(item[1],item[2],int(timestamp),labName)
        count+=1
    print("{} records uploaded".format(count))
        



# timestamp = {'.sv':'timestamp'}
# reading ={'date': timestamp, 'temp':20, 'humi':40}
# status = db.child("measurement").push(reading)
# print(status)
# measurement = db.child('measurement').order_by_child('date').start_at(5).get()

# # print(measurement)
# data = measurement.val()
# # print(type(data[0]))
# for item in data:
#     print(data[item])

