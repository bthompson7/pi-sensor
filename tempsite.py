import Adafruit_DHT
import time,os,pymysql
from flask import Flask,render_template
from twisted.internet import reactor
from twisted.web.proxy import ReverseProxyResource
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from flask import request

app = Flask(__name__)
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4


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
   global motion_data
   motion_data = 'Currently Offline'
   db_con()
   data = getSensorData()
   results = db_get_data()
   sqlMaxMinRes = db_get_max_min()
   motion = motion_data
   #print(motion)
   return render_template("data.html", **locals())

@app.route("/motion", methods=['GET','POST'])
def motion():
   global motion_data
   motion_data = request.form['motion']
   print(motion_data)

def db_con():
    global cursor
    global db
    db = pymysql.connect("localhost","monitor","password","temps")
    cursor = db.cursor()

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
