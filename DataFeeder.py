import sys
import urllib2
from time import sleep
from numpy import median
import Adafruit_DHT as dht

# Enter Your API key here
myAPI = 'AWP4JDDGKBZ3ASBT' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

def DHT22_data():
	# Reading from DHT22 and storing the temperature and humidity
	humi, temp = dht.read_retry(dht.DHT22, 23)
	humi += 15
	return humi, temp


def GetMedianOf(npts = 12):
	# Get median of npts DHT22  reading (default get 12 npts for 60 second)
	dataHumi = []
	dataTemp = []
	for x in range(0,npts):
		humi, temp = DHT22_data()

		# if Reading is valid
		if not (isinstance(humi, float) and isinstance(temp, float)):
			x -= 1
			print("Error Reading, try again")

		dataHumi.append(humi)
		dataTemp.append(temp)

		# Wait DHT22 to get data (minimum 2 seconds)
		sleep(5)

	return median(dataHumi), median(dataTemp)

while True:
	try:
		humi, temp = GetMedianOf()

		# If Reading is valid
		if isinstance(humi, float) and isinstance(temp, float):
			# Formatting to two decimal places
			humi = '%.2f' % humi
			temp = '%.2f' % temp

			# Sending the data to thingspeak
			conn = urllib2.urlopen(baseURL + '&field1=%s&field2=%s' % (temp, humi))
			print(conn.read())
			# Closing the connection
			conn.close()

		else:
			print('Error')

		# DHT22 requires 2 seconds to give a reading, so make sure to add delay of above 2 seconds.
		# sleep(60)

	except:
		break
