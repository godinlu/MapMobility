import folium
from folium.plugins import HeatMap
from tqdm import tqdm
from src.data import Data
from src.train_graph import TrainGraph
from src.time_grid import TimeGrid
from datetime import datetime

class Map:
    def __init__(self, gare_id:str, date:datetime, location=[45.75, 4.85], zoom_start=7) -> None:
        #on créer un instance d'une carte folium
        self.carte = folium.Map(location=[45.75, 4.85], zoom_start=7)
        self._data = Data.get_instance()
        self._train_graph = TrainGraph(gare_id, date)
        self._date = date
        self._gare_id = gare_id

        #on dessine les contour de la region auvergne rhônes alpes
        folium.GeoJson(self._data.get_aura()).add_to(self.carte)

    def add_gare(self) -> None:
        """
        Cette fonction ajoute un point jour sur la carte pour chaque gare
        """
        color = "gray"
        for index, row in self._data.get_stops().iterrows():
            if (row['stop_id'] == self._gare_id):
                color = "red"
                popup = self._train_graph.get_list_station()[row['stop_id']]
            elif (row['stop_id'] in self._train_graph.get_list_station().keys() ):
                color = "green"
                popup = self._train_graph.get_list_station()[row['stop_id']]
            else:
                color="white"
                popup = row['stop_name']

            folium.CircleMarker([row['stop_lat'], row['stop_lon']], radius=5, color=color, fill=True, fill_color='blue', popup=popup).add_to(self.carte)

    def add_trajet(self) -> None:
        """
        Cette fonction ajoute un trait reliant 2 gares pour chaque trajet
        """
        train_graph = TrainGraph()
        stops = self._data.get_stops()


        for edge in tqdm(train_graph.graph.edges(), desc = "adding edge in the map"):
            gare_a = stops[stops["stop_id"] == edge[0]].iloc[0]
            gare_b = stops[stops["stop_id"] == edge[1]].iloc[0]
            folium.PolyLine([(gare_a['stop_lat'], gare_a['stop_lon']), (gare_b['stop_lat'], gare_b['stop_lon'])], color="blue").add_to(self.carte)


    def add_heatmap(self)->None:
        time_grid = TimeGrid(self._train_graph.get_list_station())

        HeatMap(time_grid.get_grid(),min_opacity=0.2,max_opacity = 0.3).add_to(self.carte)
    
    def save(self, name="carte_auvergne_rhone_alpes")->None:

        #print(self.carte._repr_html_().split('</script>')[-1])
        self.carte.save(name + '.html')




