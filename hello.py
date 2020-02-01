import Adafruit_DHT
import time,os,pymysql
from flask import Flask,render_template
from twisted.internet import reactor
from twisted.web.proxy import ReverseProxyResource
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

app = Flask(__name__)

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

def db_get_data():
    try:
        sqlSelect = "SELECT * FROM tempdata2 ORDER BY id desc limit 10" #order by id limit 10
        cursor.execute(sqlSelect)
        res = cursor.fetchall()
    except:
        print("Error fetching data")
    return res

@app.route('/data')
def hello_world():
   db_con()
   data = getSensorData()
   results = db_get_data()
   sqlMaxMinRes = db_get_max_min()
   return render_template("data.html", **locals())

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

def test():
   print("Alert sent")
   os.system("curl https://notify.run/45HwVDLxNxptvaMe -d 'Temp dropped below 50'")


def getSensorData():
        global results
        humd, temp = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
        if humd is not None and temp is not None:
            tempToFair = (temp * 1.8) + 32.0
            tempRounded = round(tempToFair,2)
            sqlInsert = ("""INSERT INTO tempdata2 (temp,humd) VALUES(%d,%d)"""%(tempRounded,humd))
            try:
                cursor.execute(sqlInsert)
                db.commit()
            except:
                db.rollback()
                print("Error inserting data")
            if tempToFair < 50.0:
               test()
            return ("Temp: %s 'F Humdity: %s %%"%(tempRounded,humd))
        else:
           return "Sensor Error, refresh the page"



flask_site = WSGIResource(reactor, reactor.getThreadPool(), app)
root = Resource()
root.putChild(b'my_flask', flask_site)
site_example = ReverseProxyResource('www.example.com', 80, '/')
root.putChild('data', site_example)
reactor.listenTCP(5000, Site(root))
reactor.run()

