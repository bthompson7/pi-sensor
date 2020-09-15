import RPi.GPIO as GPIO
import time
import datetime
import requests
import json

time.sleep(60)
motion = 0
def detect():
	motion = 0
	while True:
		if GPIO.input(7) == True:
			motion+=1
			if motion >= 8:
				data = str(datetime.datetime.now()) + " Lots of motion detected "
				time.sleep(60)
			else:
				data = str(datetime.datetime.now()) + " Motion detected " + str(motion) + " times "

		else:
			data = str(datetime.datetime.now()) + " No motion detected"
			motion = 0

		myobj = {'motion': data}
		json.dumps(myobj)
		print(myobj)
		try:
			x = requests.post("http://192.168.1.2:5000/motion" ,data=myobj)
			print(x.text)
			time.sleep(0.5)
		except:
			time.sleep(600)

if __name__ == "__main__":
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7,GPIO.IN)
	detect()
	GPIO.cleanup()
