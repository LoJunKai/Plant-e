import json
import os
import numpy as np
import matplotlib.pyplot as plt

path = r'C:\Users\JK\Desktop'
os.chdir(path)

light = np.array([])
moisture = np.array([])

with open('Plant-e-00002103.json') as json_file:
    data = json.load(json_file)
    plant_e = data['Plant-e']
    # plant_e --> 100    {'day 0': {'0': {'light': 13.333333333333334, ... 
    #             101    {'day 0': {'0': {'light': 13.333333333333334, ...
    nan_count = 0
    for i in plant_e.values():
        # i --> {'day 0': {'0': {'light': 13.333333333333334, ... 
        for hours in i.values():
            # hours --> (either)
            # {'0': {'light': 13.333333333333334, 'moisture': 91}, '1': {'light': 14.166666666666668, 'moisture': 89}, '17': {'light': 1239.1666666666667, 'moisture': 87}, '18': {'light': 252.5, 'moisture': 86}, '19': {'light': 250.83333333333334, 'moisture': 85}, '20': {'light': 15.0, 'moisture': 85}, '21': {'light': 2.5, 'moisture': 85}, '22': {'light': 2.5, 'moisture': 84}, '23': {'light': 2.5, 'moisture': 84}}
            # [{'light': 2.5, 'moisture': 85}, {'light': 2.5, 'moisture': 85}, {'light': 2.5, 'moisture': 85}, {'light': 2.5, 'moisture': 85}, None, {'light': 0.0, 'moisture': 85}, {'light': 0.0, 'moisture': 84}, {'light': 15.0, 'moisture': 84}, None, {'light': 345.0, 'moisture': 84}, {'light': 475.0, 'moisture': 84}, {'light': 480.0, 'moisture': 83}, None, {'light': 871.6666666666667, 'moisture': 84}, {'light': 749.1666666666667, 'moisture': 84}, {'light': 749.1666666666667, 'moisture': 84}, {'light': 1042.5, 'moisture': 84}, None, {'light': 154.16666666666669, 'moisture': 86}, {'light': 8.333333333333334, 'moisture': 86}, {'light': 0.8333333333333334, 'moisture': 86}, {'light': 0.8333333333333334, 'moisture': 86}, {'light': 0.8333333333333334, 'moisture': 86}, {'light': 1.6666666666666667, 'moisture': 86}]
            if type(hours) == dict:
                for hour in hours.items():
                    # hour --> ('0', {'light': 13.333333333333334, ...
                    light = np.append(light, int(hour[1]['light']))
                    moisture = np.append(moisture, hour[1]['moisture'])
            elif type(hours) == list:
                for j in hours:
                    if j == None:
                        nan_count += 1
                    else:
                        np.append(light, int(j['light']))
                        np.append(moisture, j['moisture'])

plt.hist(light)
plt.show()
plt.hist(moisture)
plt.show()

plt.plot(light)
plt.show()
plt.plot(moisture)
plt.show()