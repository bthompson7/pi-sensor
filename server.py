import Adafruit_DHT
import time,os,pymysql
from flask import Flask,render_template
from twisted.internet import reactor
from twisted.web.proxy import ReverseProxyResource
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from flask import request,Response,redirect,url_for
from send import *
import datetime
import pytz,sys
import threading
from flask_caching import Cache

app = Flask(__name__)
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
sema = threading.Semaphore()

config = {
    "DEBUG": False,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app.config.from_mapping(config)
cache = Cache(app)

if len(sys.argv) > 2:
    print('You have specified too many arguments')
    sys.exit()

if len(sys.argv) < 2:
   print('You need to supply more arguments')
   sys.exit()


is_maintenance_mode = sys.argv[1]

@app.before_request
def check_for_maintenance():
   if is_maintenance_mode == 'True' and request.path != url_for('maintenance') and request.remote_addr != '192.168.1.6':
      print("Maintenance mode enabled! Request from ",request.remote_addr)
      return redirect(url_for('maintenance'))

#get 10 most recent readings
def db_get_data():
    try:
        sqlSelect = "SELECT * FROM tempdata2 ORDER BY id desc limit 10"
        cursor.execute(sqlSelect)
        res = cursor.fetchall()
    except:
        print("Error fetching data")
    return res

@app.route('/')
def main():
   print("Request for / from ",request.remote_addr)
   db_con()

   global motion_data
   global temp_data1
   global temp_data2

   results = db_get_data()

   try:
      temp1 = temp_data1
   except:
      temp1 = None

   try:
      motion = motion_data
   except:
      motion = None

   try:
      temp2 = temp_data2
   except:
      temp2 = None

   return render_template("data.html", **locals())

#this function handles incoming http post request from the temp/humd sensor on the pi that runs the server
#this is so that temp/humd alerts can be sent out
@app.route("/temp1",methods=['POST'])
def temp1():
   db_con()
   #we will get a response like: ImmutableMultiDict([('humd', '61.0'), ('temp', '69.8')])
   global temp_data1
   data = request.form
   temp = data['temp']
   humd = data['humd']
   temp_data1 = "Temp: " + temp + " Humd: " + humd

   if temp is None or humd is None:
      return {"response":"bad request"},400
   print("working...")
   temp = float(temp)
   humd = float(humd)

   try:
      print("inserting data")
      sqlInsert = ("""INSERT INTO tempdata2 (temp,humd) VALUES(%d,%d)"""%(float(temp),float(humd)))
      cursor.execute(sqlInsert)
      db.commit()
      print("insert was successful!")

   except:

      db.rollback()
      print("Error inserting data")

   #send out temp alert if we need to
   if temp < 60.0:
      print("The temp has fallen below an acceptable range send an alert")
      x = threading.Thread(target=email, args=("Temp has fallen below an acceptable range. The last reading was: ",temp_data1,))
      x.start()
   return {"response":"ok"},200

#this function handes incoming http post requests from another remote temp/humd sensor
@app.route("/temp2",methods=['POST'])
def temp2():
   global temp_data2
   temp_data2 = request.form['tempdata']
   if temp_data2 is None:
      return {"response":"bad request"},400
   return {"response":"ok"},200

#handles incoming http post requests from the remote motion sensor
@app.route("/motion", methods=['POST'])
def motion():
   global motion_data
   motion_data = request.form['motion']
   now = datetime.datetime.now(pytz.timezone('US/Eastern'))
   hour = int(now.hour)
   if "Lots of motion detected" in motion_data and (hour == 23 or hour == 00 or hour >= 1 and hour <= 5): #Email Alerts are active between 11PM - 6 AM
      print("Lots of motion detected sending alert...")
      x = threading.Thread(target=email, args=("Lots of motion detected",motion_data,))
      x.start()
   return {"response": "200"}, 200

@app.route('/chart')
@cache.cached(timeout=300) #300 seconds = 5 mins
def chart():
   print("Request for /chart from ", request.remote_addr)
   db_con()
   select_temp_data = "select * from(select * from tempdata2 order by id desc limit 50)Var1 order by id asc"
   cursor.execute(select_temp_data)
   data2 = cursor.fetchall()
   x_val = [id[0] for id in data2]
   y_val = [temp[1] for temp in data2] #temp
   y_val2 = [humd[2] for humd in data2] #humd
   return render_template("chart.html",**locals())

@app.route('/maintenance')
def maintenance():
   return render_template("503.html"), 503

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def db_con():
    global cursor
    global db
    db = pymysql.connect("localhost","monitor","password","temps")
    cursor = db.cursor()

def email(email_msg,sensor_data):
   email = EmailSender()
   email.sendEmail(email_msg,sensor_data)


def db_get_max_min():
    sqlMaxMin = "SELECT * FROM tempdata2 order by temp asc"
    cursor.execute(sqlMaxMin)
    sqlRes = cursor.fetchall()
    return sqlRes

def getSensorData():
        global results
        humd, temp = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
        if humd is not None and temp is not None:
            tempToFar = (temp * 1.8) + 32.0
            tempRounded = round(tempToFar,2)
            sqlInsert = ("""INSERT INTO tempdata2 (temp,humd) VALUES(%d,%d)"""%(tempRounded,humd))
            try:
                cursor.execute(sqlInsert)
                db.commit()
            except:
                db.rollback()
                print("Error inserting data")
            return ("Temp: %s 'F Humdity: %s %%"%(tempRounded,humd))
        else:
           return "Sensor Error, refresh the page"

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)
reactor.listenTCP(5000, site)
reactor.run()
