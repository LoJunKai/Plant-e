#import RPi.GPIO as GPIO
import pyrebase
import datetime
tz = datetime.timezone(datetime.timedelta(hours=8)) # can add name='SGT' to change %Z from UTC+0800 to SGT
import serial
import smbus
import base64
from picamera import PiCamera
import time
import database  # Download the file database.py

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

user, db = database.setup()

"""---------------PLEASE DELETE THOSE THAT WE ARE NOT USING!!----------------"""

#Define some constants from the datasheet
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


"""
Crontab 101:

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

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return int(result)

def readLight(addr=LDR[0]):
  """Reads light value for each plant"""

  #Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def readMoisture(plant):
    """ returns moisture level for each plant """
    moisture = None
    ser = serial.Serial("/dev/ttyACM0", 9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600

    for _ in range(20):
        ser.write(b'%d'%plant)
        ser.flush()
        if ser.in_waiting > 0:
            val = ser.readline()
            val = val.replace(b'\r', b'')
            val = val.replace(b'\n', b'')
            if val == b'':
                continue
            moisture = ord(val)
            break
        time.sleep(1)

    return moisture

LDR = (0x23, 0x5c) # LDR[0] = Default device I2C address, LDR[1] = set as per instructions below
def getdata(plant):
    """ return {"light" : 123, "moisture" : 321} picture is in rpi camera code """
    
    index = {100:0, 101:1, 102:2, 104:3, 110:4, 111:5}
    plant = index[plant]
    
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
    with PiCamera() as camera:
        camera.start_preview()
        camera.capture('/home/pi/Desktop/day{}.jpg'.format(day))
        camera.stop_preview()
    with open("/home/pi/Desktop/day{}.jpg".format(day), "rb") as imageFile:
        imgbytes = base64.b64encode(imageFile.read())
        imgstr = imgbytes.decode('utf-8')
        db.child("Camera").child("day " + str(day)).set(imgstr, user['idToken'])
    return


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
            date_3["day " + str(i)] = date_dict.get(date[i], [None])
            # [None] --> skip the day when it has no data
            # Eg. Day1, day2, day 4 (day3 no data) when called on day5, it will return average of day 4, day2

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
        cal_ave3(db, plant, "day " + str(day))
