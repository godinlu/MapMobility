from src.train_graph import TrainGraph
import pandas as pd
from src.utils import get_bike_time
from src.routes_stops import Routes_stops
import geopandas as gpd
from shapely.geometry import Point

def test_graph() :


    stop_times = pd.read_csv('data/stop_times.txt')
    stop_times = stop_times[stop_times['stop_id'].str.contains('Train')]
    train_graph = TrainGraph(stop_times)

    print(train_graph.graph)
    print(train_graph.graph2)


    gare_1 = 'StopPoint:OCETrain TER-87726802'
    gare_2 = 'StopPoint:OCETrain TER-87747006'

    #print(train_graph.get_time_between(gare_1, gare_2)/60)
    #print(train_graph.get_dijkstra(gare_1))
    #train_graph.show()


def test_map():
    routes_stops = Routes_stops()
    route_id = 'FR:Line::05C666F4-3B26-4DB6-A4A8-F3C6D6150B76:'
    print(routes_stops.get_arret_routes(route_id))

    coord1 = (45.77671, 3.08819)  # Coordonnées de Paris, France
    coord2 = (44.19582, 5.72788)  # Coordonnées de Londres, Royaume-Uni
    print(get_bike_time(coord1, coord2) /60)
    #aura.save()


## test Loc
def point_dans_region_auvergne_rhone_alpes(latitude, longitude, fichier_geojson):
    # Charger le fichier GeoJSON de la région Auvergne-Rhône-Alpes
    region_auvergne_rhone_alpes = gpd.read_file(fichier_geojson)

    # Créer un objet Point avec les coordonnées du point
    point = Point(longitude, latitude)

    # Vérifier si le point est à l'intérieur de la région Auvergne-Rhône-Alpes
    est_dans_region = point.within(region_auvergne_rhone_alpes.geometry.iloc[0])

    return est_dans_region