from src.data import Data
from scipy.spatial import KDTree
from src.utils import meters_projection, get_bike_time
import pandas as pd

class TimeGrid:
    def __init__(self,dict_station:dict, k=1) -> None:
        self._aura_grid = Data.get_instance().get_grid_AURA()
        self._stops = Data.get_instance().get_stops()


        dict_station = pd.DataFrame({'stop_id':dict_station.keys(),'time':dict_station.values() })
        self._stops =  pd.merge(self._stops,  pd.DataFrame(dict_station), on='stop_id',how='inner')
        self.create_station_dist()
        



    def create_station_dist(self) -> None:
        stops_2D = self._stops.apply(lambda row:meters_projection(row['stop_lon'], row['stop_lat']), axis=1).to_list()
        #print(stops_2D)
        # points_gares = list(  zip(self._stops['stop_lat'], self._stops['stop_lon']))
        # print(points_gares)

        kdtree_328 = KDTree(stops_2D)
        distances, indices = kdtree_328.query(self._aura_grid['2D'])
        distances =  list(map(get_bike_time, distances))

        print(pd.DataFrame(distances).describe())

        for i in range(len(distances)):
            distances[i] = [
                
                self._aura_grid['3D'][i][1],
                self._aura_grid['3D'][i][0],
                self._stops.loc[indices[i],'time']  + distances[i]
                ] 
        self._grid = distances
        print(pd.DataFrame(self._grid).describe())

    def get_grid(self) -> list[list[float]]:
        return self._grid



