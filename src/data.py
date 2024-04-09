import pandas as pd
import json
from shapely.geometry import Point, Polygon
from src.stop_times_manager import StopTimesManager
from src.utils import meters_projection
import numpy as np
import geopandas as gpd
from tqdm import tqdm
import os


class Data:
    """
    Cette classe singleton sert à faire tous les imports de fichiers de données csv pour éviter 
    d'avoir plusieurs lecture de données à des endroits différents
    """
    _instance = None
    AURA_GRID_PATH = 'data/AURA_grid.json'

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


    def get_grid_AURA(self) ->dict[str,list[list[float]]]:
        if not os.path.exists(self.AURA_GRID_PATH):
            self.create_grid_AURA()
        
        with open(self.AURA_GRID_PATH, "r") as json_file:
            return json.load(json_file) 

    
    def create_grid_AURA(self, length:int = 1000, height:int = 800) -> None:
        X_arr = np.linspace(self._region_aura.bounds.min()['minx'],self._region_aura.bounds.min()['maxx'],length)
        Y_arr = np.linspace(self._region_aura.bounds.min()['miny'],self._region_aura.bounds.min()['maxy'],height)

        with open('./data/region-auvergne-rhone-alpes.geojson') as f:
            geojson_data = json.load(f)
        region_polygon = Polygon(geojson_data['geometry']['coordinates'][0])

        aura_grid = {'3D':[], '2D':[]}
        for x in tqdm(X_arr):
            for y in Y_arr:
                if region_polygon.contains(Point(x,y)):
                    aura_grid['3D'].append((x,y))
                    aura_grid['2D'].append( meters_projection(x, y) )

        with open(self.AURA_GRID_PATH, "w") as file:
            json.dump(aura_grid, file)



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