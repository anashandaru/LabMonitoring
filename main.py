from DataRead import GetMedianOf
from Database import InsertToDB
from FirebaseLink import upload

humi, temp = GetMedianOf()
# humi, temp = DHT22_data()
timestamp = InsertToDB(humi, temp)
upload(humi, temp, timestamp)
print('temperature: {0:.2f}  humidity: {1:.2f}'.format(temp,humi))