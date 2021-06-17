# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 21:06:25 2021
@TODO change dont use coordinates as param with defualt argumnets

@author: samue
"""
from __future__ import unicode_literals
from simplekml import Kml, ColorMode, AltitudeMode, Style, Color
import GeoData
import socket
import time
import json


class Area():
    def __init__(self, kml, name='Restricted Area', description='', coordinates=[]):
        self.style = Style()
        self.style.linestyle.width = 5
        self.style.linestyle.color = Color.red
       
        area = kml.newpolygon(name=name, description=description, outerboundaryis=coordinates)
        area.style = self.style
    
class Path():
    def __init__(self, kml, name='', coordinates=[]):
        if not isinstance(coordinates, list):
            coordinates = [coordinates]
        self.coords = coordinates
        lineCoords = coordinates
        pointCoord = []
        if(coordinates):
            pointCoord = coordinates[-1]
        
        self.pointStyle = Style()
        # self.pointStyle.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/arrow.png'
        
        self.lineStyle = Style()
        self.lineStyle.linestyle.color = Color.blue
        self.lineStyle.linestyle.width = 4
        
        self.point = kml.newpoint(name=name, description='Actual Position', coords=[pointCoord])
        self.point.style = self.pointStyle
        
        self.line = kml.newlinestring(name=name, coords=lineCoords)
        self.line.style = self.lineStyle
        
        
    def addCoordinate(self, coordinate):
        self.coords.append(coordinate)
        if len(self.coords) >= 2:
            self.point.coords = [self.coords[-1]]
        else:
             self.point.coords = self.coords
        self.line.coords = self.coords
        


# Create an instance of Kml
kml_area = Kml(name="Basics", open=1)
kml_path = Kml(name="Basics", open=1)

# Create a new document
doc_area = kml_area.newdocument(name="Pedalo viewer")
doc_path = kml_area.newdocument(name="Pedalo viewer")

area = list()
path_data = list()
path_kml = list()

d = GeoData.GeoData('3_ResArea_2Rides.kml')
for name, area in d['Polygons'].items():
    area.append(Area(kml_area, description=name, coordinates=area))
    
for name, area in d['LineStrings'].items():
    path_data.append({'name':name, 'data':area})

for elem in path_data:
    path_kml.append(Path(kml_path, elem['name'], elem['data'][0]))
    # create kml object
    # path_kml.append(Path(kml_path, elem['name']))


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        count = 1
        time.sleep(5)
        
        while True:
            if count == 1:
                data = kml_area.kml().encode("ascii", "ignore").decode()
                data = {'kmlData':data, 'region':True, 'warning':False}
                conn.sendall(json.dumps(data).encode("ascii", "ignore"))
            else:
                for dataElem, kmlElem in zip(path_data, path_kml):
                    for coord in dataElem['data']:
                        print(coord)
                        kmlElem.addCoordinate(coord)
                        d = kml_path.kml().encode("ascii", "ignore").decode()
                        d = {'kmlData':d, 'region':False, 'warning':False}
                        conn.sendall(json.dumps(d).encode("ascii", "ignore"))
                        time.sleep(1)
                        
                    
                # for path in path_kml:
                #     for elem in path_data:
                #         for data in elem['data']:
                #             path.addCoordinate(data)
                #             # print(data)
                #             d = kml_path.kml().encode("ascii", "ignore").decode()
                #             d = {'kmlData':d, 'region':False, 'warning':False}
                #             conn.sendall(json.dumps(d).encode("ascii", "ignore"))
                #             time.sleep(1)
            
            time.sleep(1)
            count += 1

      
