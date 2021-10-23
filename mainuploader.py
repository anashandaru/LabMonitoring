from Database import InsertToDB
from FirebaseLink import upload

f = open("/home/pi/labmonstate.log","r")
read = f.read()
read = read.split(',')
humi = float(read[0])
temp = float(read[1])
time = float(read[2])
timestamp = InsertToDB(humi, temp, time)
upload(humi, temp, timestamp)
