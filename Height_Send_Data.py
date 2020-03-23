#import RPi.GPIO as GPIO
#from time import sleep
import pyrebase
import datetime
tz = datetime.timezone(datetime.timedelta(hours=8)) # can add name='SGT' to change %Z from UTC+0800 to SGT
#import serial
#import smbus
#import base64
#from picamera import PiCamera

#camera = PiCamera()

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


#MEASURE HIGHEST POINT
#change value of height for each day in cm

day = "day 0"   #change day number accordingly

db.child("Height").child("100").child(day).set(9.3, user['idToken'])
db.child("Height").child("101").child(day).set(11.3, user['idToken'])
db.child("Height").child("102").child(day).set(2.9, user['idToken'])
db.child("Height").child("104").child(day).set(13.1, user['idToken'])
db.child("Height").child("110").child(day).set(10.8, user['idToken'])
db.child("Height").child("111").child(day).set(1.4, user['idToken'])

#run the code and the database should be updated