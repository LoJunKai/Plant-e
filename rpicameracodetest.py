from picamera import PiCamera
from time import sleep
import base64

camera = PiCamera()

#saving captured pic to db

#import RPi.GPIO as GPIO
#from time import sleep
import pyrebase


projectid = "plant-e"
dburl = "https://" + projectid + ".firebaseio.com"
authdomain = projectid + ".firebaseapp.com"
apikey = "AIzaSyDJxaq0uT1JpIkftOgjoldVIy7mT9KG844"
email = "plant-e@dw.com"
password = "afordw"
bucketurl = "plant-e.appspot.com"

config = {
    "apiKey": apikey,
    "authDomain": authdomain,
    "databaseURL": dburl,
    "storageBucket" : bucketurl,
    "serviceAccount" : "/home/pi/Desktop/plant-e-a8ad60b1326c.json"
}
# Create a firebase object by specifying the URL of the database and its secret token.
# The firebase object has functions put and get, that allows user to put data onto
# the database and also retrieve data from the database.

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)

db = firebase.database()
root = db.child("/").get(user['idToken'])


def takepic(day):
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/Desktop/day{}.jpg'.format(day))
    camera.stop_preview()
    with open("day{}.jpg".format(day), "rb") as imageFile:
        imgbytes = base64.b64encode(imageFile.read())
        imgstr = imgbytes.decode('utf-8')
        db.child("Camera").child("day " + str(day)).set(imgstr, user['idToken'])
    return

takepic(0)
print("Done")

