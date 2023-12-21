import json
from shapely.geometry import Point, Polygon

class Region:
    """
    Cette classe sert à manager la Region auvergne rhone alpes
    avec le geo_json 
    """
    AURA_PATH = 'data/region-auvergne-rhone-alpes.geojson'
    _geo_gson = None
    _polygon:Polygon = None

    @staticmethod
    def is_in_region(lattitude:float, longitude:float)->bool:
        """
        Cette fonction renvoie vrai si le point est dans la region auvergne rhone alpes
        et faux sinon
        """
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
