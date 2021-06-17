# -*- coding: utf-8 -*-
"""
Created on 09.03.2021
@TODO: add the ability to add data 

store data as kml and dict

adjust format so that the regions also have a name not only 
a description

The GeoData class allows the 
Script to handle kml files.
Issue: fastkml sometimes changes between shapely and pygeo
@author: Samuel Niederer
"""


from fastkml import kml
# from pygeoif.geometry import Point, LineString, Polygon
from shapely.geometry import Point, LineString, Polygon

class GeoData():
    """
    A class to represent geo data from a kml file.

    ...

    Attributes
    ----------

    Methods
    -------
   
    """
    
    def __init__(self, path):
        """ Parse a kml file and extract the coordinates """
        self.data = {}
        dataStr = ""
        with open(path, 'rt', encoding="utf-8") as f: 
            dataStr = f.read()

        k = kml.KML()
        k.from_string(dataStr)
        outerFeatures = list(k.features())
        features = list(outerFeatures[0].features())
        
        polygons = {}
        lineStrings = {}
        points = {}
        
        for f in features:
            if isinstance(f.geometry, Polygon):
                coord = [elem for elem in f.geometry.exterior.coords]
                polygons.update({f.description:coord})
                
            if isinstance(f.geometry, LineString):
                coord = [elem for elem in f.geometry.coords]
                lineStrings.update({f.description:coord})
                
            if isinstance(f.geometry, Point):
                coord = [elem for elem in f.geometry.coords]
                points.update({f.name:coord})
                
        self.data.update({'Polygons':polygons})
        self.data.update({'LineStrings':lineStrings})
        self.data.update({'Points':points})
        
    def __str__(self):
        string = ""
        for k, v in self.data.items():
            string += f"{k}: \n"
            string += 20*'-' + '\n'
            for key, value in v.items():
                string += f"{key}: \n"
                string += '\n'.join([f"{elem[0]} : {elem[1]}" for elem in value])
                string += '\n\n'
        
        return string 
    
    def __getitem__(self, key):
        return self.data[key]

    
if __name__ == '__main__':
    d = GeoData("checkPointInPolygon.kml")
    
    pointIn =  d['Points']['Point_Inside']
    pointOut = d['Points']['Point_outside']
    area = d['Polygons']['VierEck']
    
    for name, area in d['Polygons'].items():
        print(name)
        print(area)
    print()
    print(d)



