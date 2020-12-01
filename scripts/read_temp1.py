import Adafruit_DHT,time,requests,json


#pin setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

#sleep for 300 seconds(5 minutes) to wait for the server to start
#this is incase power is lost and the entire system needs to reboot
time.sleep(300)

while True:
	humd, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	print(humd)
	print(temp)
	if humd is not None and temp is not None:
		try:
			tempToFair = (temp * 1.8) + 32.0
			tempRounded = round(tempToFair,4)
			print("Temp = %s F Humditiy = %s"%(tempRounded,humd))
			tempData = {"temp":tempRounded,"humd":humd}
			json.dumps(tempData)
			print("Sending request to server")
			x = requests.post("http://192.168.1.2:5000/temp1",data=tempData)
			print(x.text)
		except:
			print("request failed sleeping. The server must be down")
			time.sleep(600)
	else:
		print("Error reading data nothing was sent.")

	time.sleep(600) #600 seconds = 10 minutes
