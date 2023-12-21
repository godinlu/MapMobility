import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

class TrainGraph:
    def __init__(self, df_stops_times:pd.DataFrame) -> None:
        self.graph = nx.MultiDiGraph()

        # for nom_gare in df_stops_times.drop_duplicates(subset='stop_id')['stop_id']:
        #     self.graph.add_node(nom_gare)
        trip_ids = df_stops_times.drop_duplicates(subset='trip_id')['trip_id']
        for trip_id in trip_ids:
            ligne = df_stops_times[df_stops_times['trip_id'] == trip_id]

            for i in range(len(ligne)):
                print(ligne.iloc[i])


        # for _, row in df_stops_times.iterrows():
        #     trip_id, arrival_time, departure_time, stop_id, stop_sequence = row[['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence']]

        #     # Ajouter les nœuds (gares) au graphe
        #     if not self.graph.has_node(stop_id):
        #         self.graph.add_node(stop_id)
            
        #     # Ajouter les arêtes (lignes) au graphe avec le temps comme poids
        #     time_difference = pd.to_datetime(departure_time) - pd.to_datetime(arrival_time)
        #     print(time_difference.total_seconds())

        #     if self.graph.has_edge(stop_id, trip_id):
        #         # Si l'arête existe déjà, mettez à jour le poids avec le temps de trajet minimum
        #         current_weight = self.graph[stop_id][trip_id]['weight']
        #         new_weight = min(current_weight, time_difference.total_seconds())
        #         self.graph[stop_id][trip_id]['weight'] = new_weight
        #     else:
        #         self.graph.add_edge(stop_id, trip_id, weight=time_difference.total_seconds())

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

        