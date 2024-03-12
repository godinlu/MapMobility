import folium
from src.data import Data
from src.train_graph import TrainGraph

class Map:
    def __init__(self, location=[45.75, 4.85], zoom_start=7) -> None:
        #on créer un instance d'une carte folium
        self.carte = folium.Map(location=[45.75, 4.85], zoom_start=7)
        self._data = Data.get_instance()

        #on dessine les contour de la region auvergne rhônes alpes
        folium.GeoJson(self._data.get_aura()).add_to(self.carte)

    def add_gare(self) -> None:
        """
        Cette fonction ajoute un point jour sur la carte pour chaque gare
        """
        for index, row in self._data.get_stops().iterrows():
            folium.CircleMarker([row['stop_lat'], row['stop_lon']], radius=5, color='red', fill=True, fill_color='blue', popup=row['stop_name']).add_to(self.carte)

    def add_trajet(self) -> None:
        """
        Cette fonction ajoute un trait reliant 2 gares pour chaque trajet
        """
        train_graph = TrainGraph()
        stops = self._data.get_stops()

        for edge in train_graph.graph.edges():
            gare_a = stops[stops["stop_id"] == edge[0]].iloc[0]
            gare_b = stops[stops["stop_id"] == edge[1]].iloc[0]
            folium.PolyLine([(gare_a['stop_lat'], gare_a['stop_lon']), (gare_b['stop_lat'], gare_b['stop_lon'])], color="blue").add_to(self.carte)


    
    def save(self, name="carte_auvergne_rhone_alpes")->None:
        self.carte.save(name + '.html')



