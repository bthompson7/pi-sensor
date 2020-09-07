import Adafruit_DHT,time,requests,json


#pin setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

while True:
	humd, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	if humd is not None and temp is not None:
		tempToFair = (temp * 1.8) + 32.0
		tempRounded = round(tempToFair,4)
		print("Temp = %s F Humditiy = %s"%(tempRounded,humd))
		tempData = {"temp":tempRounded,"humd":humd}
		json.dumps(tempData)
		x = requests.post("http://192.168.1.2:5000/temp1",data=tempData)
		print(x.text)
	else:
		print("post request failed!")
		tempData = {"error":"Sensor error refresh the page"}
		json.dumps(tempData)
		x = requests.post("http://192.168.1.2:5000/temp1",data=tempData)
		print(x.text)

	time.sleep(600) #600 seconds = 10 minutes
