"""
Created on Thu Mar 18 09:11:52 2021
@author: Samuel Niederer

Call this program with comandline arguments like shown in the example below:
    Example command: python fileName.py long:lat:pedaloID

The programm will append the received coordinates and store it in a local json file
Then the data gets proccesed and stored in a kml file which gets finally printed 
"""

import sys
import json    
from simplekml import Kml
from KMLcreater import Path

# load data from local file
data = []
with open('data.json') as json_file:
    data = json.load(json_file)

# append data received through arguments       
for arg in sys.argv:
    msg = arg.split(':')
    if len(msg) == 3:
        long = msg[0]
        lat = msg[1]
        name = msg[2]
        coords = [float(long), float(lat)]
        
        if name in data.keys():
            data[name].append(coords)
        else:
            data.update({name:[coords]})

# save data to local file
with open('data.json', 'w') as json_file:
    json.dump(data, json_file)

    
# Create an instance of Kml
kml = Kml(name="Basics", open=1)
# Create a new document
doc = kml.newdocument(name="Pedalo viewer")
# area = list()
path = list()

for name in data.keys():
    path.append(Path(kml, name=name, coordinates=data[name]))

# print kml file -> send it to javascript caller
print(kml.kml().encode("ascii", "ignore").decode())
# kml.save('test.kml')



