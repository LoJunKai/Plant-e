"""
Just import this file and call it

import database
user, db = database.setup('<project name>') --> "plant-e" or "veggie-e"
"""

import pyrebase

def setup(projectid):
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
	    # "storageBucket": "plant-e.appspot.com"
	}
	# Create a firebase object by specifying the URL of the database and its secret token.
	# The firebase object has functions put and get, that allows user to put data onto
	# the database and also retrieve data from the database.

	firebase = pyrebase.initialize_app(config)
	auth = firebase.auth()
	user = auth.sign_in_with_email_and_password(email, password)

	return user, firebase.database()