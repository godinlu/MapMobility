from src.data import Data
from scipy.spatial import KDTree
import pandas as pd

class TimeGrid:
    def __init__(self,dict_station:dict, k=1) -> None:
        self._aura_grid = Data.get_instance().get_grid_AURA()
        self._stops = Data.get_instance().get_stops()

        self._stops = self._stops[self._stops['stop_id'].isin(dict_station.keys())]
        self.create_station_dist()
        



    def create_station_dist(self) -> None:
        points_gares = list(zip(self._stops['stop_lat'], self._stops['stop_lon']))
        kdtree_328 = KDTree(points_gares)
        distances, indices = kdtree_328.query(self._aura_grid)
        print(indices)