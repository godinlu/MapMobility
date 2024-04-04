import pandas as pd
import json
from shapely.geometry import Point, Polygon
from src.stop_times_manager import StopTimesManager
import geopandas as gpd

class Data:
    """
    Cette classe singleton sert à faire tous les imports de fichiers de données csv pour éviter 
    d'avoir plusieurs lecture de données à des endroits différents
    """
    _instance = None

    @staticmethod
    def get_instance():
        if Data._instance is None:
            Data._instance = Data()
        return Data._instance
    
    def __init__(self) -> None:
        if Data._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to obtain an instance.")
        
        self._stops = pd.read_csv("data/stops.txt")
        self._stop_times = pd.read_csv("data/stop_times.txt")
        self._trips = pd.read_csv("data/trips.txt")
        self._routes = pd.read_csv("data/routes.txt")
        
        self._stop_times_manager = StopTimesManager()

        self._region_aura = gpd.read_file("data/region-auvergne-rhone-alpes.geojson")

        self.preprocess_data()

    def preprocess_data(self) -> None:
        """
        cette fonction enlèves les données superflue comme les bus et
        garde que les points de auvergne rhone alpes
        """
        #on commence par garder que les gare de trains
        self._stops = self._stops[self._stops['stop_id'].str.contains('Train')]

        #ensuite on garde que les gare qui sont dans auvergne rhâne alpes
        gdf_stops = gpd.GeoDataFrame(self._stops, geometry=gpd.points_from_xy(self._stops['stop_lon'], self._stops['stop_lat']))
        mask = gdf_stops.within(self._region_aura.geometry.unary_union)
        self._stops = self._stops[mask]

        #puis on garde que les trajet qui passent par les gares selectionné précédemment
        self._stop_times = self._stop_times[self._stop_times['stop_id'].isin(self._stops['stop_id'])]



    def get_stops(self) -> pd.DataFrame:
        return self._stops
    
    def get_stop_times(self, weekday:int) -> pd.DataFrame:
        return self._stop_times_manager.get_stop_times(weekday)
    
    def get_trips(self) -> pd.DataFrame:
        return self._trips
    
    def get_routes(self) -> pd.DataFrame:
        return self._routes
    
    def get_aura(self) -> any:
        return self._region_aura