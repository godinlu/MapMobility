import folium
import geojson
import json
from shapely.geometry import shape, Point
def is_inside(coord, gjson):
    for feature in gjson['features']:
        forme_shapely = shape(feature['geometry'])
        point = Point(coord)
        if point.within(forme_shapely):
            return True
    return False

#ouvrir le geojson
chemin = "region-auvergne-rhone-alpes.geojson"
with open(chemin, 'r') as f:
    data = json.load(f)
point1 = [45.75,4.85]

print(is_inside(data,point1))