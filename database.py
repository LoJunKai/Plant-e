# Setup database using:
# user, db = db_setup('<project name>') --> "plant-e" or "veggie-e"

import pyrebase
import datetime
import time
import json

#######################################################################
# Timing functions
#######################################################################

tz = datetime.timezone(datetime.timedelta(hours=8)) # can add name='SGT' to change %Z from UTC+0800 to SGT

def get_time():
    """ returns current time """

    nowtime = datetime.datetime.now(tz)
    return nowtime


def get_day(db, user, plant):
    """ returns day number for each plant """

    #plantdata = db.child("Init Time").get(plant, user['idToken']).val()
    #init_time_str = plantdata["init time"]
    init_time_str = db.child("Init Time").child(plant).child("init time").get(user['idToken']).val()      # get string in database under plant's "Init Time"
    init_time = datetime.datetime.strptime(init_time_str + ' UTC+0800','%d-%m-%Y %X %Z%z')          # convert string to datetime object
    nowday = get_time() - init_time
    return nowday.days


def get_hour(db, user, plant):
    """ returns hour count for each plant """

    nowtime = get_time().strftime('%d-%m-%Y %X')
    currenthour = int(nowtime[11:13])
    db.child("Init Time").child(plant).child("hour").set(currenthour, user['idToken'])
    hour = db.child("Init Time").child(plant).child("hour").get(user['idToken']).val()
    return hour

#######################################################################
# Data functions
#######################################################################

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


# Call this function at the start of every new day to get the average of light and moisture data of the past 3 days
def cal_ave3(db, user, plant, current_date):
	# current_date is the date to be populated (just reach day 4, current_date == 'day 4')
	if int(current_date[-1]) < 3:
		print("current_date not above 3")
		return None

	# returns the last 3 days of the data_dict
	def last_3_days(date_dict, current_date):
		# returns {'day 0':[list of dicts...], 'day 1':[...], 'day 2':[...]}
		date = []
		for i in range(3):
			date.append(current_date[:-1] + str(int(current_date[-1]) - i - 1))
		date = date[::-1]

		date_3 = {}
		for i in range(len(date)):
			date_3["day " + str(i)] = date_dict[date[i]]

		return date_3

	def average(date_3):
		light = 0
		moisture = 0
		counter = 0
		for list_of_dicts in date_3.values():
			# list_of_dicts --> [{'light': 123, 'moisture': 321}, None, {'light': 234, 'moisture': 542}]
			# if there is only 1 dict stored, list_of_dicts --> {'<index>': {'light': 847, 'moisture': 274}}
			for dicts in list_of_dicts:
				# Skip missing data
				if dicts == None:
					continue
				# Account when there is only 1 dict stored
				if type(dicts) == str:
					dicts = list_of_dicts[dicts] # assigns dicts with {'light': 847, 'moisture': 274}
				light += dicts["light"]
				moisture += dicts["moisture"]
				counter += 1

		return int(light/counter), int(moisture/counter)


	# Get plant data from firebase
	date_dict = db.child("Plant-e").child(plant).get(user['idToken']).val()
	# date_dict.val() --> OrderedDict([('day 0', [{'light': 123, 'moisture': 321}, {'light': 837, 'moisture': 658}, {'light': 234, 'moisture': 542}]), ('day 1', [None, {'light': 342, 'moisture': 632}])])

	date_3 = last_3_days(date_dict, current_date)
	light, moisture = average(date_3)

	# Populate Ave3 node
	dd = {"light":light, "moisture":moisture}
	db.child("Ave3").child(plant).child(current_date).set(dd, user['idToken'])

	return None
