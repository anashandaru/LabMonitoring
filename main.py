from DataRead import DHT22_data
#from Database import InsertToDB
#from FirebaseLink import upload
from datetime import datetime
from tftdisplay import update
import time
import board
import adafruit_dht
dhtDevice = adafruit_dht.DHT22(board.D14)

while True:
    now = datetime.now()
    humi, temp = DHT22_data(dhtDevice)
    update(humi, temp)
    f = open("/home/pi/labmonstate.log","w")
    f.write("{},{},{}".format(humi, temp, datetime.timestamp(now)))
    print('temperature: {0:.2f}  humidity: {1:.2f}'.format(temp,humi))
    time.sleep(5)
#timestamp = InsertToDB(humi, temp)
#upload(humi, temp, timestamp)
