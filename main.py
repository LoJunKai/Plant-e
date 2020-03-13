#import RPi.GPIO as GPIO
#from time import sleep
import pyrebase
import datetime
tz = datetime.timezone(datetime.timedelta(hours=8)) # can add name='SGT' to change %Z from UTC+0800 to SGT
import serial
import smbus
import base64
from picamera import PiCamera
import time

camera = PiCamera()

projectid = "plant-e"
dburl = "https://" + projectid + ".firebaseio.com"
authdomain = projectid + ".firebaseio.com"

apikey = "AIzaSyDJxaq0uT1JpIkftOgjoldVIy7mT9KG844"
email = "plant-e@dw.com"
password = "afordw"

config = {
    "apiKey": apikey,
    "authDomain": authdomain,
    "databaseURL": dburl,
    "storageBucket": "plant-e.appspot.com"
}
# Create a firebase object by specifying the URL of the database and its secret token.
# The firebase object has functions put and get, that allows user to put data onto
# the database and also retrieve data from the database.

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)

db = firebase.database()
root = db.child("/").get(user['idToken'])


"""
crontab -e                                               #select editor
0 * * * * python3 /home/pi/<insertfilename>              # min  hour  day_of_month  month  day_of_week  command
replacing your command with      sudo reboot now         #this makes your rpi restart anytime the scheduled task runs
crontab -l   <-- not sure if 1 or l                      #to view file without editing
"""


def gettime():
    """ returns current time """

    nowtime = datetime.datetime.now(tz)
    return nowtime

def getday(plant):
    """ returns day number for each plant """

    #plantdata = db.child("Init Time").get(plant, user['idToken']).val()
    #init_time_str = plantdata["init time"]
    init_time_str = db.child("Init Time").child(plant).child("init time").get(user['idToken']).val()      # get string in database under plant's "Init Time"
    init_time = datetime.datetime.strptime(init_time_str + ' UTC+0800','%d-%m-%Y %X %Z%z')          # convert string to datetime object
    nowday = gettime() - init_time
    return nowday.days

def gethour(plant):
    """ returns hour count for each plant """

    nowtime = gettime().strftime('%d-%m-%Y %X')
    currenthour = int(nowtime[11:13])
    db.child("Init Time").child(plant).child("hour").set(currenthour, user['idToken'])
    hour = db.child("Init Time").child(plant).child("hour").get(user['idToken']).val()
    return hour

def readMoisture(plant):
    """ returns moisture level for each plant """
    print("reading moisture...")
    ser = serial.Serial("/dev/ttyACM0", 9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    moisture = ser.readline()[:-1]   
    moisturels = list(map(ord, moisture.split()))
    print(moisturels)
    moisture = moisturels[plant]
    return moisture

#Define some constants from the datasheet

LDR        = (0x23, 0x5c) # LDR[0] = Default device I2C address, LDR[1] = set as per instructions below

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=LDR[1]):
  """Reads light value for each plant"""

  #Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def getdata(plant):
    """ return {"light" : 123, "moisture" : 321} picture is in rpi camera code """

    index = {100:0, 101:1, 102:2, 104:3, 110:4, 111:5}

    plant = index[plant]
    print(plant)
    
    if plant == 0 or plant == 1 or plant == 2:
    	ldr = LDR[0]
    else:
    	ldr = LDR[1]

    data = {"light" : readLight(ldr), "moisture" : readMoisture(plant)}
    return data

def senddata(data, plant, day, hourcount):
    """ sends received data to database """

    db.child("Plant-e").child(plant).child("day " + str(day)).child(hourcount).child("light").set(data["light"], user['idToken'])           # stores light value in database
    db.child("Plant-e").child(plant).child("day " + str(day)).child(hourcount).child("moisture").set(data["moisture"], user['idToken'])     # store moisture value in database

def getallplantls():
    """ returns ordered dictionary of keys and values under Names """

    plantdic = db.child("Names").get(user['idToken']).val()
    print(plantdic)
    return plantdic

def takepic(day):
    camera.start_preview()
    camera.capture('/home/pi/Desktop/day{}.jpg'.format(day))
    camera.stop_preview()
    with open("day{}.jpg".format(day), "rb") as imageFile:
        imgbytes = base64.b64encode(imageFile.read())
        imgstr = imgbytes.decode('utf-8')
        db.child("Camera").child("day " + str(day)).set(imgstr, user['idToken'])
    return

allplantls = getallplantls()
for plant in allplantls:
    if plant == None:
        continue
    plant = int(plant)
    day = getday(plant)
    hourcount = gethour(plant)
    data = getdata(plant)
    senddata(data, plant, day, hourcount)
    if hourcount == 1:
        takepic(day)
    #    average()

'''

'''



'''
    if hourcount == 24:
        hourcount = 0
    
    if getday(init_time) == day:
        senddata(data, plant, day, hourcount)
        hourcount += 1
    else:
        day += 1
        senddata(data, plant, day, hourcount)
        hourcount += 1
'''


#dd = {"light" : 123, "moisture" : 321, "camera" : "picture"}
#db.child("Plant-e").child(0).child("day 0").child(0).set(dd, user['idToken'])


"""    
    init_time_str = datetime.datetime.now(tz).strftime('%d-%m-%Y %X')  # convert to string to store in database
    db.child("InitTime").set(init_time_str, user['idToken'])  # store string in database under "initTime"
    init_time = datetime.datetime.strptime(init_time_str + ' UTC+0800', '%d-%m-%Y %X %Z%z')  # convert string to datetime object
    
"""
