import folium
from tqdm import tqdm
from src.data import Data
from src.SPG import SPG
from datetime import datetime

class Map2:
    def __init__(self, gare_id:str, date:datetime, location=[45.75, 4.85], zoom_start=7) -> None:
        #on créer un instance d'une carte folium
        self.carte = folium.Map(location=[45.75, 4.85], zoom_start=7)
        self._data = Data.get_instance()
        self._SPG = SPG(gare_id, date)
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
                popup = self._SPG.get_list_station()[row['stop_id']]
            elif (row['stop_id'] in self._SPG.get_list_station().keys() ):
                color = "green"
                popup = self._SPG.get_list_station()[row['stop_id']]
            else:
                color="white"
                popup = row['stop_name']

            folium.CircleMarker([row['stop_lat'], row['stop_lon']], radius=5, color=color, fill=True, fill_color='blue', popup=popup).add_to(self.carte)

    
    def save(self, name="carte_auvergne_rhone_alpes")->None:
        self.carte.save(name + '.html')



