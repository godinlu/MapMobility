import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from .utils import heures_en_secondes

class TrainGraph:
    def __init__(self, df_stops_times:pd.DataFrame) -> None:
        self.graph = nx.MultiDiGraph()

        for _, trip in tqdm(df_stops_times.groupby('trip_id'), desc="Processing trips"):

            for i in range(len(trip) - 1):
                first_stop = trip.iloc[i]
                next_stop = trip.iloc[i+1]
                time_difference = heures_en_secondes(next_stop['arrival_time']) -  heures_en_secondes(first_stop['departure_time'])
                self.graph.add_edge(first_stop['stop_id'], next_stop['stop_id'], weight=time_difference)

        
    def get_shortest_path(self, id_stop_start:str, id_stop_end:str)->int:
        """
        Cette fonction renvoie le temps en seconde du plus cours chemin entre 2 stop
        """
        shortest_path = nx.shortest_path(self.graph, id_stop_start, id_stop_end)
        cumulative_weight = sum(self.graph[shortest_path[i]][shortest_path[i+1]][0]['weight'] for i in range(len(shortest_path)-1))
        return cumulative_weight


    def show(self)->None:
        # Visualisation du graphe
        pos = nx.spring_layout(self.graph)  # Vous pouvez choisir un autre algorithme de disposition
        nx.draw(self.graph ,pos)
        # Ajout des étiquettes des arêtes directement sur le graphique
        labels = nx.get_edge_attributes(self.graph, 'weight')
        for edge, weight in labels.items():
            x, y = pos[edge[0]]
            label_x = (x + pos[edge[1]][0]) / 2
            label_y = (y + pos[edge[1]][1]) / 2
            plt.text(label_x, label_y, f"{weight:.2f}", fontsize=8, color='red')

        plt.show()

        