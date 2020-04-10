# Make sure you have run pip install -r requirements.txt to download the necessary dependencies

"""
Crontab 101:

crontab -e                                               #select editor
0 * * * * python3 /home/pi/<insertfilename>              # min  hour  day_of_month  month  day_of_week  command
replacing your command with      sudo reboot now         #this makes your rpi restart anytime the scheduled task runs
crontab -l   <-- not sure if 1 or l                      #to view file without editing
"""

from database import *
from sensors import *
from camera import takepic
import smbus

# Change accordingly if SMBus error occurs
# bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

# Setup database
user, db = db_setup("plant-e")

# Get I2C address using: sudo i2cdetect -y 1
LDR = (0x23, 0x5c)  # LDR[0] = Default device I2C address, LDR[1] = set as per instructions below


# Get data from the sensors
def get_data(plant):
    """ return {"light" : 123, "moisture" : 321} picture is in rpi camera code """

    index = {100: 0, 101: 1, 102: 2, 104: 3, 110: 4, 111: 5}
    plant = index[plant]

    if plant == 0 or plant == 1 or plant == 2:
        ldr = LDR[0]
    else:
        ldr = LDR[1]

    data = {"light": read_light(bus, ldr), "moisture": read_moisture_arduino(plant)}
    return data


if __name__ == '__main__':
    # Get all plants and iterate through each plant to update all plants
    allplantls = get_all_plant_ls(db, user)
    for plant in allplantls:

        # Sometimes the database returns None, so just skip those values
        if plant is None:
            continue
        plant = int(plant)

        # Get time
        day = get_day(db, user, plant)
        hourcount = get_hour(db, user, plant)

        # Get sensor data and send it to database
        data = get_data(plant)
        send_data(db, user, data, plant, day, hourcount)

        if hourcount == 1:
            # Code in here is scheduled to be run daily at <hourcount>
            take_pic(db, user, day)
            cal_ave3(db, user, plant, "day " + str(day))
