import Adafruit_DHT
import time,os,json
from flask import Flask,render_template
from flaskext.mysql import MySQL

from twisted.internet import reactor
from twisted.web.proxy import ReverseProxyResource
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from flask import request,Response,redirect,url_for,jsonify
import datetime
import pytz,sys
import threading
from flask_caching import Cache

app = Flask(__name__)

sema = threading.Semaphore()

#database information
global mysql
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'monitor'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'temps'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#cache config
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
   if is_maintenance_mode == 'True' and request.path != url_for('maintenance'):
      print("Maintenance mode enabled! Request from ",request.remote_addr)
      return redirect(url_for('maintenance'))

@app.route('/')
def main():
   print("Request for / from ",request.remote_addr)
   return render_template("data.html")

#this function handles incoming http post request from the temp/humd sensor on the pi that runs the server
#this is so that temp/humd alerts can be sent out
@app.route("/updateTemp1",methods=['POST'])
def temp1():
   db_connect()
   global temp_data1
   data = request.form
   temp = data['temp']
   humid = data['humd']

   temp_data1 = data

   if temp is None or humid is None:
      return {"response":"bad request"},400
   temp = float(temp)
   humid = float(humid)

   try:
      sqlInsert = ("""INSERT INTO tempdata2 (temp,humd,date) VALUES(%d,%d,NOW())"""%(temp,humid))
      cursor.execute(sqlInsert)
      db.commit()

   except Exception as e:
      db.rollback()
      print("Error in /updateTemp1 endpoint", e)
      return jsonfiy(e), 500

   tempInfo = "Temp is %s and Humidity is %s"%(temp,humid)
   return {"response":"200"},200

#this function handes incoming http post requests from another remote temp/humd sensor
@app.route("/updateTemp2",methods=['POST'])
def temp2():
   db_connect()
   global temp_data2
   data = request.form
   temp = data['temp']
   humid = data['humd']

   temp_data2 = data

   if temp is None or humid is None:
      return {"response":"Data contains no information"},400

   temp = float(temp)
   humid = float(humid)

   try:

      sqlInsert = ("""INSERT INTO tempdata3 (temp,humd,date) VALUES(%d,%d,NOW())"""%(temp,humid))
      cursor.execute(sqlInsert)
      db.commit()

   except Exception as e:
      db.rollback()
      print("Error in /updateTemp2 endpoint", e)
      return jsonify(e), 500

   return {"response":"200"},200


@app.route("/updateSumpLevel")
def updateSumpLevel():
    try:
        water_level = request.form['water_level']
        db_connect()
        sqlInsert = ("""INSERT INTO sometable (water_level,date) VALUES(%d,NOW())"""%(water_level))
        cursor.execute(sqlInsert)
        db.commit()

    except Exception as e:
        db.rollback()
        print("Error in /updateSumpLevel ", e)
        return jsonify(e),500

    return {"response":"200"},200


#handles incoming http post requests from the remote motion sensor
@app.route("/updateMotion", methods=['POST'])
def motion():

   global motion_data
   motion_data = request.form['motion']
   now = datetime.datetime.now(pytz.timezone('US/Eastern'))
   hour = int(now.hour)
   return {"response":"200"}, 200

@app.route("/getTemp1", methods=['GET'])
def getTemp1():
	try:
		db_connect()
		select1 = "select temp,humd from tempdata2 order by id desc limit 1"
		cursor.execute(select1)
		db.commit()
		tempData1 = cursor.fetchall()

	except Exception as e:
		db.rollback()
		print("Error in /getTemp1 endpoint", e)
		return jsonify(e), 500

	return jsonify(tempData1), 200

@app.route("/getTemp2", methods=['GET'])
def getTemp2():
	try:
		db_connect()
		select2 = "select temp,humd from tempdata3 order by id desc limit 1"
		cursor.execute(select2)
		db.commit()
		tempData2 = cursor.fetchall()

	except Exception as e:
		db.rollback()
		print("Error in /getTemp2 endpoint", e)
		return jsonify(e), 500

	return jsonify(tempData2), 200


@app.route('/temp1Chart')
@cache.cached(timeout=600) #600 seconds = 10 mins
def chart1():
   db_connect()
   print("Request for /chart from ", request.remote_addr)
   select_temp_data = "select * from(select * from tempdata2 order by id desc limit 50)Var1 order by id asc"
   cursor.execute(select_temp_data)
   data2 = cursor.fetchall()
   x_val = [date[3] for date in data2]
   y_val = [temp[1] for temp in data2] #temp
   y_val2 = [humd[2] for humd in data2] #humd
   page_title = "Basement Sensor Chart"
   return render_template("chart.html",**locals())

@app.route('/temp2Chart')
@cache.cached(timeout=600) #600 seconds = 10 mins
def chart2():
   db_connect()
   print("Request for /chart from ", request.remote_addr)
   select_temp_data = "select * from(select * from tempdata3 order by id desc limit 50)Var1 order by id asc"
   cursor.execute(select_temp_data)
   data2 = cursor.fetchall()
   x_val = [date[3] for date in data2]
   y_val = [temp[1] for temp in data2] #temp
   y_val2 = [humd[2] for humd in data2] #humd
   page_title = "Bedroom Sensor Chart"
   return render_template("chart.html",**locals())



@app.route('/maintenance')
def maintenance():
   return render_template("503.html"), 503

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def db_connect():
    sema.acquire()
    global db
    global cursor

    try:
        db = mysql.get_db()
        cursor = db.cursor()
    except:
        print("error connecting to the database.")
    finally:
        sema.release()

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)
reactor.listenTCP(5000, site)
reactor.run()
