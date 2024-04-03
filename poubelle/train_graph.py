

import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from ..src.utils import heures_en_secondes
from ..src.data import Data
from datetime import datetime

class TrainGraph:
    def __init__(self) -> None:
        """
        Lorsque l'on créer 
        """
        self.graph = nx.MultiDiGraph()
        df_stops_times = Data.get_instance().get_stops_times()

        for _, trip in tqdm(df_stops_times.groupby('trip_id'), desc="Processing trips"):

            for i in range(len(trip) - 1):
                first_stop = trip.iloc[i]
                next_stop = trip.iloc[i+1]
                time_difference = heures_en_secondes(next_stop['arrival_time']) -  heures_en_secondes(first_stop['departure_time'])
                self.graph.add_edge(first_stop['stop_id'], next_stop['stop_id'], weight=time_difference)
        
                
    def get_shortest_path(self, id_stop_start:str, id_stop_end:str)->list:
        """
        Cette fonction renvoie le chemin le plus court entre les deux gares
        """
        return nx.shortest_path(self.graph, id_stop_start, id_stop_end)
        
    def get_time_between(self, id_stop_start:str, id_stop_end:str, date:datetime)->int:
        """
        Cette fonction renvoie le temps en seconde du plus cours chemin entre 2 stop
        """
        shortest_path = self.get_shortest_path(id_stop_start, id_stop_end)
        print(shortest_path)
        stop_times = Data.get_instance().get_stops_times()

        #on fait un premier filtre pour garder que les lignes avec les arrêts concerné
        stop_times = stop_times[stop_times['stop_id'].isin(shortest_path)]

        #
        stop_times = stop_times[
            stop_times['trip_id'].apply(lambda x: datetime.fromisoformat(x.split(':')[1]).weekday()) == date.weekday()
        ]
        
        print(stop_times)
    
    def get_dijkstra(self, id_source_stop:str):
        return nx.single_source_dijkstra_path_length(self.graph, id_source_stop, weight='weight')
    





        