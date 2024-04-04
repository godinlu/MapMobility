import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from src.utils import heures_en_secondes
from src.data import Data
from datetime import datetime,date
from src.train_graph import TrainGraph


class SPG:
    def __init__(self,gare_id:str,start_time:datetime) -> None:
        """
        Lorsque l'on créer 
        """
        self.graph = nx.MultiDiGraph()
        self.df_stops_times = Data.get_instance().get_stop_times(start_time.weekday())
        self.df_stops = Data.get_instance().get_stops()
        self.list_gare = {}
        self.nb_err = 0

        for _, trip in tqdm(self.df_stops_times.groupby('trip_id'), desc="Processing trips"):

            for i in range(len(trip) - 1):
                first_stop = trip.iloc[i]
                next_stop = trip.iloc[i+1]
                time_difference = heures_en_secondes(next_stop['arrival_time']) -  heures_en_secondes(first_stop['departure_time'])
                self.graph.add_edge(first_stop['stop_id'], next_stop['stop_id'], weight=time_difference)
        print("ça a marché")

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
        self.get_time_station(gare_id,start_time)

        print(len(self.df_stops))
        print(len(self.list_gare))
        print(self.nb_err)
        print(len(self.df_stops_times['stop_id'].unique()))
                
    def get_shortest_path(self, id_stop_start:str, id_stop_end:str)->list:
        """
        Cette fonction renvoie le chemin le plus court entre les deux gares
        """
        
        try:
            shortest_path = nx.shortest_path(self.graph, id_stop_start, id_stop_end)
            return shortest_path
        except Exception:
            # Gérer le cas où aucun chemin n'existe
            self.nb_err = self.nb_err + 1
            return 1 # Ou une autre valeur que vous préférez pour indiquer l'absence
        
    
    def get_dijkstra(self, id_source_stop:str):
        return nx.single_source_dijkstra_path_length(self.graph, id_source_stop, weight='weight')
    
    def get_time_station(self,id_stop_start:str, start_time:datetime)->None:
        
        for index,row in self.df_stops.iterrows():
            
            if(id_stop_start!=row["stop_id"]):
                short_stations = self.get_shortest_path(id_stop_start, row["stop_id"])
                if(short_stations!=1):
                    count = 0
                    for i in short_stations:
                        
                        tmp_date = start_time
                        if(count+1<len(short_stations)):
                            if(i in self.list_gare):
                                tmp_date = self.list_gare[i]                            
                            else:
                                tmp_date = self.get_time_between_station(i,short_stations[count+1],tmp_date)
                                self.list_gare[i] = tmp_date
                        count = count+1

    def get_time_between_station(self,id_station_1,id_station_2,start_time:datetime)->datetime:
        indices = self.get_indice_station_2(id_station_1,id_station_2,start_time)
        time_between = self.df_stops_times.loc[indices]['arrival_time'].min()
        return time_between


    def get_indice_station_2(self, id_station_1,id_station_2,  start_time:datetime)->list:
        '''
        Cette fonction renvoie les indices des gares suivantes dans un trajet du dataframe. 
        '''
        #trie sur la gare_id et l'heure
        index = ( 
                    (self.df_stops_times['stop_id'] == id_station_1) &
                    (self.df_stops_times['departure_time'].apply(lambda x: datetime.fromisoformat(x).time()) > start_time.time()) 
                )
        indices = self.df_stops_times[index].index.tolist()
        indice_next_stations = []

        for i in indices:
            if (i+1 < self.df_stops_times.shape[0] and
                self.df_stops_times.at[i+1, 'trip_id'] == self.df_stops_times.at[i, 'trip_id'] and
                self.df_stops_times.at[i+1,'stop_id'] == id_station_2):
                indice_next_stations.append(i+1)
        return indice_next_stations


    def get_list_station(self)->dict:
        return self.list_gare



        