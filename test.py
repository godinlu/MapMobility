#from src.train_graph import TrainGraph
from src.train_graph import TrainGraph


import pandas as pd
from src.utils import get_bike_time
from src.data import Data
from src.map import Map
from datetime import datetime
import geopandas as gpd
from shapely.geometry import Point

def test_graph() :
    train_graph = TrainGraph()


    gare_1 = 'StopPoint:OCETrain TER-87726802'
    gare_2 = 'StopPoint:OCETrain TER-87747006'



    #print(train_graph.get_time_between(gare_1, gare_2)/60)
    #print(train_graph.get_dijkstra(gare_1))
    print(train_graph.get_time_between(gare_1, gare_2, datetime(2024, 4, 2)))
    #train_graph.show()

def test_graph_v2() :
    train_graph = TrainGraph('StopPoint:OCETrain TER-87726802', datetime(2024,4,2,6,0,0))



def test_map():
    map = Map()
    map.add_gare()
    map.add_trajet()
    map.save()

def test_data():
    data = Data.get_instance()
    print(data.get_stops_times())



## test Loc
def point_dans_region_auvergne_rhone_alpes(latitude, longitude, fichier_geojson):
    # Charger le fichier GeoJSON de la région Auvergne-Rhône-Alpes
    region_auvergne_rhone_alpes = gpd.read_file(fichier_geojson)

    # Créer un objet Point avec les coordonnées du point
    point = Point(longitude, latitude)

    # Vérifier si le point est à l'intérieur de la région Auvergne-Rhône-Alpes
    est_dans_region = point.within(region_auvergne_rhone_alpes.geometry.iloc[0])

    return est_dans_region



if __name__ == "__main__":
    test_graph_v2()