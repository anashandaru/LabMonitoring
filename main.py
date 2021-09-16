from DataRead import GetMedianOf
from Database import InsertToDB

humi, temp = GetMedianOf()
# humi, temp = DHT22_data()
InsertToDB(humi, temp)
print('temperature: {0:.2f}  humidity: {1:.2f}'.format(temp,humi))