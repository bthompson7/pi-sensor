
import Adafruit_DHT,time,requests,json

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

#sleep for 300 seconds(5 minutes) to wait for the server to start
#this is incase power is lost and the entire system needs to reboot
time.sleep(300)

#time between sensor readings
time_delay = 600 #default is 600 seconds / 10 minutes
error_delay = 600
in_event_mode = False

while True:
	humd, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	print(humd)
	print(temp)
	if humd is not None and temp is not None:
		try:
			tempToFahr = (temp * 1.8) + 32.0
			tempRounded = round(tempToFahr,4)

			#if temp is at 40 degrees or lower go into event mode, meaning pipes in the basement are in danger of freezing
			#eventually I would like to add some sort of alarm here maybe play some mp3 file on a speaker
			if tempRounded <= 40:
				time_delay = 60
				in_event_mode = True
			elif tempRounded > 40 and in_event_mode:
				in_event_mode = False

			print("Temp = %s F Humditiy = %s"%(tempRounded,humd))
			tempData = {"temp":tempRounded,"humd":humd}
			json.dumps(tempData)
			print("Sending request to server")
			x = requests.post("http://192.168.1.2:5000/temp1",data=tempData)
			print(x.text)
		except:
			print("request failed sleeping. The server must be down")
			time.sleep(error_delay)
	else:
		print("Error reading data nothing was sent.")

	time.sleep(time_delay)
