# Code for getting the average of light and moisture data of the past 3 days

import pyrebase
import datetime, json

tz = datetime.timezone(datetime.timedelta(hours=8)) # can add name='SGT' to change %Z from UTC+0800 to SGT


# Call this function at the start of every new day to input the 3 days ave for that day
def cal_ave3(db, plant, current_date):
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
