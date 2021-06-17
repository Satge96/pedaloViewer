"""
TODO: create class with linestyles for point line and polygon,

"""
from __future__ import unicode_literals
from simplekml import Kml, ColorMode, AltitudeMode, Style, Color

class Area():
    def __init__(self, kml, name='Restricted Area', description='', coordinates=[]):
        self.style = Style()
        self.style.linestyle.width = 5
        self.style.linestyle.color = Color.red
       
        area = kml.newpolygon(name=name, description=description, outerboundaryis=coordinates)
        area.style = self.style
    
class Path():
    def __init__(self, kml, name, coordinates):
        if not isinstance(coordinates, list):
            coordinates = [coordinates]
        self.coords = coordinates
        lineCoords = coordinates
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
        self.point.coords = [self.coords[-1]]
        self.line.coords = self.coords
        

if __name__ == '__main__':  
    # Create an instance of Kml
    kml = Kml(name="Basics", open=1)
    
    # Create a new document
    doc = kml.newdocument(name="Pedalo viewer")
    
    area = list()
    path = list()
    """
    d = GeoData.GeoData('3_ResArea_2Rides.kml')
    for name, area in d['Polygons'].items():
        area.append(Area(kml, description=name, coordinates=area))
        
    for name, area in d['LineStrings'].items():
        path.append(Path(kml, name=name, coordinates=area))
    """
    # coords = d['LineStrings']['Pedalo_1']
    # p = Path(kml, name='Pedalo_1', coordinates=coords[0])
    # for i in range(len(coords)-5):
    #     p.addCoordinate(coords[i+1])
                   
    # kml.save('../node/leaflet-kml/public/assets/E01Basic-custom.kml')
    # kml.save('test.kml')
    print(kml.kml().encode("ascii", "ignore").decode())
