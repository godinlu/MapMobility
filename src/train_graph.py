from .data import Data
import pandas as pd
from datetime import datetime, time, timedelta, date

class TrainGraph:
    def __init__(self, gare_id:str, start_time:datetime) -> None:
        self.list_gare = {}
        self.iter = 0
        self.df_stops_times = Data.get_instance().get_stops_times()

        #on commence par conserver seulement les trip qui correspondent au jour de la semaine
        self.df_stops_times = self.df_stops_times[
            self.df_stops_times['trip_id'].apply(lambda x: datetime.fromisoformat(x.split(':')[1]).weekday()) == start_time.weekday()
        ]

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

        self.propagation(gare_id, start_time)
        

    def propagation(self, gare_id:str, start_time:datetime) -> None:
        #cas d'arret lorsqu'il existe un meilleur temps pour allé à la gare
        if (gare_id in self.list_gare and self.list_gare[gare_id] < start_time ):
            return;

        #cas simple de propagation avec les autres gares
        self.list_gare[gare_id] = start_time
        indices_next_stations = self.get_next_stations(gare_id, start_time)

        min_group = self.df_stops_times.loc[indices_next_stations].groupby('stop_id')['arrival_time'].min()

        for stop_id, min_date in min_group.items():
            self.propagation(stop_id, datetime.fromisoformat(min_date) )

    def get_next_stations(self, gare_id:str,  start_time:datetime)->list:
        '''
        Cette fonction renvoie les indices des gares suivantes dans un trajet du dataframe. 
        '''
        #trie sur la gare_id et l'heure
        index = ( 
                    (self.df_stops_times['stop_id'] == gare_id) &
                    (self.df_stops_times['departure_time'].apply(lambda x: datetime.fromisoformat(x).time()) > start_time.time()) 
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
    
    def get_list_station(self)->dict:
        return self.list_gare
