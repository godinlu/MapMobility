from .data import Data
from scipy.spatial import KDTree
from .utils import meters_projection, get_bike_time
import pandas as pd
import numpy as np

class TimeGrid:
    def __init__(self,dict_station:dict, start_coord:tuple[float, float]) -> None:
        self._aura_grid = Data.get_instance().get_grid_AURA()
        self._stops = Data.get_instance().get_stops()
        self._stops.loc[self._stops['stop_id'] == 'gare_fictive', 'stop_lat'] = start_coord[0]
        self._stops.loc[self._stops['stop_id'] == 'gare_fictive', 'stop_lon'] = start_coord[1]

        self._start_coord = start_coord

        dict_station = pd.DataFrame({'stop_id':dict_station.keys(),'time':dict_station.values() })
        self._stops =  pd.merge(self._stops,  pd.DataFrame(dict_station), on='stop_id',how='inner')
        self.create_station_dist()
        



    def create_station_dist(self) -> None:
        stops_2D = self._stops.apply(lambda row:meters_projection(row['stop_lat'], row['stop_lon']), axis=1).to_list()

        kdtree_328 = KDTree(stops_2D)
        distances, indices = kdtree_328.query(self._aura_grid['2D'])
        distances =  list(map(get_bike_time, distances))

        # Extraire les temps des arrêts de bus
        bus_stop_times = self._stops.loc[indices, 'time'].reset_index(drop=True)

        df_tmp = pd.DataFrame({'time': bus_stop_times, 'distances':distances})
        # Ajouter les distances aux temps des arrêts de bus
        self._grid = np.hstack((
            np.array(self._aura_grid['3D']),
            (df_tmp['time'] + df_tmp['distances']).to_numpy().reshape((len(distances),1))
        ))

    def get_grid(self) -> list[list[float]]:
        return self._grid.tolist()
    
    


