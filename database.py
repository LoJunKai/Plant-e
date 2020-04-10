"""
Call it using:

user, db = db_setup('<project name>') --> "plant-e" or "veggie-e"
"""

import pyrebase

def db_setup(projectid):
	# projectid = "plant-e" or "veggie-e"
	dburl = "https://" + projectid + ".firebaseio.com"
	authdomain = projectid + ".firebaseio.com"

	apikey = "AIzaSyDJxaq0uT1JpIkftOgjoldVIy7mT9KG844"
	email = projectid + "@dw.com"
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

	return user, firebase.database()

def send_data(db, user, data, plant, day, hourcount):
    """ sends received data to database """

    db.child("Plant-e").child(plant).child("day " + str(day)).child(hourcount).child("light").set(data["light"], user['idToken'])           # stores light value in database
    db.child("Plant-e").child(plant).child("day " + str(day)).child(hourcount).child("moisture").set(data["moisture"], user['idToken'])     # store moisture value in database

def get_all_plant_ls(db, user):
    """ returns ordered dictionary of keys and values under Names """

    plantdic = db.child("Names").get(user['idToken']).val()
    return plantdic
