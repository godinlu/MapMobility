import folium
import json
from src.stops import Stops
from src.utils import heures_en_secondes
from src.region import Region
from src.routes_stops import Routes_stops
from shapely.geometry import Point, Polygon
from scipy.spatial.distance import cdist
import numpy as np
import pandas as pd
from src.routes import Routes
import networkx as nx
from tqdm import tqdm
from functools import lru_cache
# Coordonnées centrales de la région Auvergne-Rhône-Alpes

stops = Stops()

stops_data = stops.get_locations_train()
# points = [
#     {"name": "Lyon", "location": [45.75, 4.85]},
#     {"name": "Clermont-Ferrand", "location": [45.78, 3.08]},
#     {"name": "Grenoble", "location": [45.19, 5.72]},
#     # Ajoutez d'autres points avec leurs coordonnées ici
# ]

# Créer la carte centrée sur la région
ma_carte = folium.Map(location=[45.75, 4.85], zoom_start=7)

# Ajouter un marqueur pour indiquer le centre
#folium.Marker([45.75, 4.85], popup='Auvergne-Rhône-Alpes').add_to(ma_carte)
# Ajouter un marqueur pour chaque point
# for point in points:
#     name = point["name"]
#     location = point["location"]
#     folium.CircleMarker(location, radius=5, color='red', fill=True, fill_color='blue', popup=name).add_to(ma_carte)


# Ajouter le GeoJSON à la carte pour afficher les contours de la région
folium.GeoJson(Region.get_geo_json()).add_to(ma_carte)
# Créer un polygone représentant les frontières de la région Auvergne-Rhône-Alpes

# Ajouter un cercle pour chaque arrêt de train dans la région Auvergne-Rhône-Alpes
for index, row in stops_data.iterrows():
    if Region.is_in_region(row['stop_lat'], row['stop_lon']):
        name = row['stop_name']
        #folium.CircleMarker([row['stop_lat'], row['stop_lon']], radius=5, color='red', fill=True, fill_color='blue', popup=name).add_to(ma_carte)

point_specifique = np.array([[45.75, 4.85]])
# Obtenez les coordonnées sous forme de tableau 2D pour cdist
arrets_coord = stops_data[['stop_lat', 'stop_lon']].values
# Calculer les distances entre le point spécifique et tous les arrêts de train
distances = cdist(point_specifique, arrets_coord, metric='euclidean')

# Trouver l'indice de la gare la plus proche
indice_plus_proche = np.argmin(distances)

# Obtenir les coordonnées de la gare la plus proche
gare_plus_proche = arrets_coord[indice_plus_proche]

# Ajouter un marqueur pour la gare la plus proche
#folium.Marker(gare_plus_proche, popup='Gare la plus proche', icon=folium.Icon(color='pink')).add_to(ma_carte)

#ajout de toutes les routes

data_frame_routes = pd.read_csv("data/routes.txt")
data_frame_stop_time = pd.read_csv("data/stop_times.txt")
data_frame_trip = pd.read_csv("data/trips.txt")
routes_stops = Routes_stops()#instance de Routes_stops
route_id_vect = Routes.get_train_id()['route_id']#train
#route_id_vect = data_frame_routes['route_id']#train + car
arret_route_vect = {}

for route_id in route_id_vect:
    if len(routes_stops.get_arret_routes(route_id))!=0:
        arret_route_vect[route_id] = routes_stops.get_arret_routes(route_id)

#print(arret_route_vect)

# Relier les arrêts par des lignes
for line_id , arret_route in arret_route_vect.items():
    for i in range(len(arret_route) - 1):
        #print(arret_route)
        points = [(arret_route[i]["stop_lat"], arret_route[i]["stop_lon"]),
                (arret_route[i + 1]["stop_lat"], arret_route[i + 1]["stop_lon"])]
        #folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(ma_carte)


#trouve les gares dans le graphe principal



#calcule du premier trajet qui relie 2 gares
id_gare_1 = "StopPoint:OCETrain TER-87723320"#venissieux
id_gare_2 = "StopPoint:OCETrain TER-87734475"


# Construction d'un graphe à partir des données
G = nx.Graph()


def temps_gare(gare_1_id,gare_2_id):
    trips_1 = data_frame_stop_time[data_frame_stop_time['stop_id']==gare_1_id]['trip_id']
    trips_2 = data_frame_stop_time[data_frame_stop_time['stop_id']==gare_2_id]['trip_id']
     # Récupération des trips communs entre les deux gares
    trips_communs = pd.merge(trips_1, trips_2, on='trip_id')['trip_id']
    temps_gare_1 =np.array([])
    temps_gare_2 =np.array([])
    for i in range(len(trips_communs) - 1):
        temps_gare_1 = np.append(temps_gare_1,heures_en_secondes(data_frame_stop_time[(data_frame_stop_time['trip_id'] == trips_communs[i]) & (data_frame_stop_time['stop_id'] == gare_1_id)]['arrival_time'].iloc[0]))
        temps_gare_2 = np.append(temps_gare_2,heures_en_secondes(data_frame_stop_time[(data_frame_stop_time['trip_id'] == trips_communs[i]) & (data_frame_stop_time['stop_id'] == gare_2_id)]['departure_time'].iloc[0]))
    

    temps_entre_gares = abs(temps_gare_1-temps_gare_2)
    temps_moyen = temps_entre_gares.mean()

    return temps_moyen

# Ajout des gares en tant que nœuds et création des arêtes pour chaque ligne
for ligne, gares in tqdm(arret_route_vect.items()):
    for i in range(len(gares) - 1):
        #print(gares)
        gare_actuelle = gares[i]['stop_id']
        prochaine_gare = gares[i + 1]['stop_id']
        
        #print(prochaine_gare)
        G.add_edge(gare_actuelle, prochaine_gare)


data_frame_stop= pd.read_csv("data/stops.txt")
# Ajout des gares à la carte
for node in G.nodes():
    #print(node)
    gare = data_frame_stop[data_frame_stop["stop_id"] == node][['stop_lat','stop_lon']].iloc[0]
    #print(gare)
    folium.CircleMarker([gare['stop_lat'], gare['stop_lon']], radius=5, color='red', fill=True, fill_color='blue', popup=node).add_to(ma_carte)

# Tracé des arêtes du graphe (itinéraires)
for edge in G.edges():
    #print(edge)
    gare_1 = data_frame_stop[data_frame_stop["stop_id"] == edge[0]][['stop_lat','stop_lon']].iloc[0]
    gare_2 = data_frame_stop[data_frame_stop["stop_id"] == edge[1]][['stop_lat','stop_lon']].iloc[0]
    #print(gare_1,gare_2)
    folium.PolyLine([(gare_1['stop_lat'], gare_1['stop_lon']), (gare_2['stop_lat'], gare_2['stop_lon'])], color="blue").add_to(ma_carte)

# Fonction pour trouver un chemin entre deux gares
def trouver_chemin_entre_deux_gares(gare_depart, gare_arrivee):
    try:
        chemin = nx.shortest_path(G, gare_depart, gare_arrivee)
        return chemin
    except nx.NetworkXNoPath:
        return None

# Exemple d'utilisation
gare_depart = 'StopPoint:OCETrain TER-87726802'
gare_arrivee = 'StopPoint:OCETrain TER-87747006'

chemin = trouver_chemin_entre_deux_gares(gare_depart, gare_arrivee)
if chemin:
    print("Chemin trouvé :", chemin)
else:
    print("Aucun chemin trouvé entre ces gares.")

for i in range(len(chemin) - 1):
    gare_1 = data_frame_stop[data_frame_stop["stop_id"] == chemin[i]][['stop_lat', 'stop_lon']].iloc[0]
    gare_2 = data_frame_stop[data_frame_stop["stop_id"] == chemin[i + 1]][['stop_lat', 'stop_lon']].iloc[0]
    
    folium.PolyLine([(gare_1['stop_lat'], gare_1['stop_lon']), 
                     (gare_2['stop_lat'], gare_2['stop_lon'])], color="green").add_to(ma_carte)
    
# Enregistrer la carte au format HTML
ma_carte.save('carte_auvergne_rhone_alpes.html')

#########