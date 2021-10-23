from time import sleep
from numpy import median
# import board
# import adafruit_dht
# dhtDevice = adafruit_dht.DHT22(board.D14)

def DHT22_data(dhtDevice):
	for i in range(10):
		try:
			# Reading from DHT22 and storing the temperature and humidity
			temp = dhtDevice.temperature
			humi = dhtDevice.humidity
			return humi, temp
		except:
			# Errors happen fairly often, DHT's are hard to read, just keep going
			sleep(2.0)
			continue
	return (0, 0)

def GetMedianOf(npts = 5):
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
		sleep(2.0)

	return median(dataHumi), median(dataTemp)


# humi, temp = GetMedianOf()
# humi, temp = DHT22_data()

# print('temperature: {0:.2f}  humidity: {1:.2f}'.format(temp,humi))