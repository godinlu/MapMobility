import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from .utils import heures_en_secondes
from .data import Data

class TrainGraph:
    def __init__(self, df_stops_times:pd.DataFrame) -> None:
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
        
    def get_time_between(self, id_stop_start:str, id_stop_end:str)->int:
        """
        Cette fonction renvoie le temps en seconde du plus cours chemin entre 2 stop
        """
        shortest_path = self.get_shortest_path(id_stop_start, id_stop_end)
        cumulative_weight = sum(self.graph[shortest_path[i]][shortest_path[i+1]][0]['weight'] for i in range(len(shortest_path)-1))
        return cumulative_weight
    
    def get_dijkstra(self, id_source_stop:str):
        return nx.single_source_dijkstra_path_length(self.graph, id_source_stop, weight='weight')





        