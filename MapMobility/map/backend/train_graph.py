from .data import Data
import pandas as pd
from datetime import datetime, time, timedelta, date
from .utils import get_bike_time_between,meters_projection,get_bike_time
from scipy.spatial import KDTree

class TrainGraph:
    def __init__(self, gare_loc:tuple[float,float], start_time:datetime) -> None:
        self.list_gare = {}
        self.df_stops_times = Data.get_instance().get_stop_times(start_time.weekday())
        self._stops = Data.get_instance().get_stops()



        self._stops.set_index('stop_id', inplace=True)
        self._stops.at['gare_fictive', 'stop_lat'] = gare_loc[0]
        self._stops.at['gare_fictive', 'stop_lon'] = gare_loc[1]

        #on ajoute la date au departure_time et au arrival_time
        vect_dates = self.df_stops_times['trip_id'].str.split(':').str[1].str[:-3]
        start_time = datetime.combine(date.fromisoformat(vect_dates.iloc[0]), start_time.time())
        self.df_stops_times.loc[:, 'departure_time'] = vect_dates + ':' + self.df_stops_times['departure_time']
        self.df_stops_times.loc[:, 'arrival_time'] = vect_dates + ':' + self.df_stops_times['arrival_time']

        #on formate les date qui sont > 23h
        index_arr = self.df_stops_times['arrival_time'].str[11:13].astype(int) > 23
        index_dep = self.df_stops_times['departure_time'].str[11:13].astype(int) > 23

        self.df_stops_times.loc[index_arr, 'arrival_time'] = self.df_stops_times.loc[index_arr, 'arrival_time'].apply(lambda x: TrainGraph.format_date(x))
        self.df_stops_times.loc[index_dep, 'departure_time'] = self.df_stops_times.loc[index_dep, 'departure_time'].apply(lambda x: TrainGraph.format_date(x))

        self.df_stops_times.reset_index(drop=True, inplace=True)


        for index, row in self._stops.iterrows():
            bike_time = get_bike_time_between(gare_loc, (row['stop_lat'], row['stop_lon']))
            self.list_gare[index] = start_time + timedelta(bike_time) 

        print(self.list_gare)
        #self.list_gare["gare_fictive"] = start_time
        #print(self.list_gare)

        self.propagation(self.list_gare.keys())
        self.set_list_to_sec(start_time)
        self._stops.reset_index(inplace=True)
        
    def propagation(self, list_id:list[str]) ->None:
        list_next_id = []
        for stop_id in list_id:
            indices_next_stations = self.get_next_stations(stop_id, self.list_gare[stop_id])
            min_group = self.df_stops_times.loc[indices_next_stations].groupby('stop_id')['arrival_time'].min()
            gare_a_loc = [self._stops.loc[stop_id,'stop_lat'], self._stops.loc[stop_id,'stop_lon']]

            for next_stop_id, min_date in min_group.items():
                
                gare_b_loc = [self._stops.at[next_stop_id,'stop_lat'], self._stops.at[next_stop_id,'stop_lon']]
                
                dt_min_date = min(
                    datetime.fromisoformat(min_date),
                    self.list_gare[stop_id] + timedelta(seconds=get_bike_time_between(gare_a_loc, gare_b_loc))
                    )

                if (next_stop_id not in self.list_gare or dt_min_date  < self.list_gare[next_stop_id] ):
                    #cas ou la récursion doit ce faire donc on ajoute l'id de la gare en question à list_next_id
                    #et on met à jour la date d'arrivé à cette gare
                    list_next_id.append(next_stop_id)
                    self.list_gare[next_stop_id] = dt_min_date 

        print(len(list_next_id))
        #si la liste de next_id n'est pas vide alors on lance une récursion
        if list_next_id:
            self.propagation(list_next_id)

    def get_next_stations(self, gare_id:str,  start_time:datetime)->list:
        '''
        Cette fonction renvoie les indices des gares suivantes dans un trajet du dataframe. 
        '''
        #trie sur la gare_id et l'heure
        index = ( 
                    (self.df_stops_times['stop_id'] == gare_id) &
                    (self.df_stops_times['departure_time'].apply(lambda x: datetime.fromisoformat(x)) > start_time) 
                )
        indices = self.df_stops_times[index].index.tolist()
        indice_next_stations = []

        for i in indices:
            if (i+1 < self.df_stops_times.shape[0] and
                self.df_stops_times.at[i+1, 'trip_id'] == self.df_stops_times.at[i, 'trip_id']):
                indice_next_stations.append(i+1)
        return indice_next_stations


    @staticmethod
    def format_date(date_str:str)->str:
        # Convertir la chaîne de caractères en objet datetime
        date_str = date_str[:11] + '0' + str(int(date_str[11:13]) - 24) + date_str[13:]
        tmp_date = datetime.fromisoformat(date_str) + timedelta(days=1)
        return (tmp_date.strftime('%Y-%m-%d:%H:%M:%S') )
    
    def set_list_to_sec(self, start_time:datetime)->None:
        """
        Cette fonction transforme les heures d'arrivé en seconde depuis le points source
        """
        for key in self.list_gare.keys():
            self.list_gare[key] = (self.list_gare[key] - start_time).total_seconds()

    def get_list_station(self)->dict:
        return self.list_gare
