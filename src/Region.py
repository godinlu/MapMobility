import json
from shapely.geometry import Point, Polygon

class Region:
    AURA_PATH = 'data/region-auvergne-rhone-alpes.geojson'
    _geo_gson = None
    _polygon:Polygon = None

    @staticmethod
    def is_in_region(longitude:float, lattitude:float)->bool:
        if not Region._polygon:
            Region.open()

        location = Point(longitude, lattitude)
        return (Region._polygon.contains(location))
    
    def get_geo_json():
        if not Region._geo_gson:
            Region.open()
        return Region._geo_gson


    @staticmethod
    def open()->None:
        with open(Region.AURA_PATH) as f:
            Region._geo_gson = json.load(f)

        Region._polygon = Polygon(Region._geo_gson['geometry']['coordinates'][0])

if __name__ == '__main__':
    print(Region.is_in_region(5.71436600,45.1926930))
