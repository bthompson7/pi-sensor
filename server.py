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
import pytz
import threading


app = Flask(__name__)
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
sema = threading.Semaphore()
is_maintenance_mode = False


@app.before_request
def check_for_maintenance():
   if is_maintenance_mode and request.path != url_for('maintenance') and request.remote_addr != '192.168.1.4':
      return redirect(url_for('maintenance'))

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
   db_con()
   global motion_data
   data = getSensorData()
   results = db_get_data()
   sqlMaxMinRes = db_get_max_min()
   try:
      motion = motion_data
   except:
      motion = "Offline"
   return render_template("data.html", **locals())

#handles incoming http post requests from the remote motion sensor
@app.route("/motion", methods=['POST'])
def motion():
   global motion_data
   motion_data = request.form['motion']
   #print(motion_data)
   now = datetime.datetime.now(pytz.timezone('US/Eastern'))
   hour = int(now.hour)
   if "Lots of motion detected" in motion_data and (hour == 23 or hour == 00 or hour >= 1 and hour <= 5): #Email Alerts are active between 11PM - 5 AM
      print("Lots of motion detected sending alert...")
      x = threading.Thread(target=email, args=(motion_data,))
      x.start()
   return {"response": "200"}, 200






@app.route('/chart')
def chart():
   #0 - id 1 - level
   db_con()
   select = "select * from(select * from well_data order by id desc limit 10)Var1 order by id asc"
   cursor.execute(select)
   data2 = cursor.fetchall()
   x_val = [id[0] for id in data2]
   y_val = [level[1] for level in data2]
   print(x_val)
   print(y_val)

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

def email(motion):
   email = EmailSender()
   email.sendEmail(motion)

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
