import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

while True:
	humd, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	if humd is not None and temp is not None:
		tempToFair = (temp * 1.8) + 32.0
		tempRounded = round(tempToFair,4)
		print("Temp = %s F Humditiy = %s"%(tempRounded,humd))
	else:
		print("Sensor error")
	#print("Humdity = %s"%humd)
	time.sleep(10)
