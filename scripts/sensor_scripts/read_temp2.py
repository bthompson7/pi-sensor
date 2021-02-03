
import Adafruit_DHT,time,requests,json

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#time between sensor readings
time_delay = 600 #default is 600 seconds / 10 minutes
error_delay = 600
in_event_mode = False

#in case we lose power wait for the router and everything else to come back online
time.sleep(time_delay)

while True:
	humid, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	if humid is not None and temp is not None:
		try:
			tempToF = (temp * 1.8) + 32.0
			tempRounded = round(tempToF,4)
			humidRounded = round(humid,4)

			#if temp is at 40 degrees or lower go into event mode, meaning pipes in the basement are in danger of freezing
			#eventually I would like to add some sort of alarm here maybe play some mp3 file on a speaker
			if tempRounded <= 40 and in_event_mode == False:
				time_delay = 60
				in_event_mode = True
			elif tempRounded <= 40 and in_event_mode:
				print("In Event Mode")
			elif tempRounded > 40 and in_event_mode:
				in_event_mode = False
				time_delay = 600

			print("Temp = %s F Humditiy = %s"%(tempRounded,humidRounded))
			tempData = {"temp":tempRounded,"humd":humidRounded}
			json.dumps(tempData)
			print("Sending request to server")
			x = requests.post("http://192.168.1.2:5000/updateTemp2",data=tempData)
			print(x.text)
		except:
			print("request failed sleeping. The server must be down")
			time.sleep(error_delay)
	else:
		print("Error reading data nothing was sent.")

	time.sleep(time_delay)
