# Thank you for the hardwork!

# MEASURE HIGHEST POINT
# Change value of height for each day in cm

day = "day 100"   # CHANGE DAY NUMBER ACCORDINGLY

#run the code and the database will be updated

height = {
    "100": 123123,  # Plant 1
    "101": 123123,  # Plant 2
    "102": 123123,  # Plant 3
    "104": 123123,  # Plant 4
    "110": 123123,  # Plant 5
    "111": 123123   # Plant 6
}


# Main Code:
def update(day, height):
    for plant_id, plant_height in height.items():
        db.child("Height").child(plant_id).child(day).set(plant_height, user['idToken'])




# Set up


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


update(day, height)
