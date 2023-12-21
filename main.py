import folium
import json
from src.stops import Stops
from src.region import Region
from src.routes_stops import Routes_stops
from shapely.geometry import Point, Polygon
from scipy.spatial.distance import cdist
import numpy as np
import pandas as pd

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
folium.Marker([45.75, 4.85], popup='Auvergne-Rhône-Alpes').add_to(ma_carte)
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
    if Region.is_in_region(row['stop_lon'], row['stop_lat']):
        name = row['stop_name']
        folium.CircleMarker([row['stop_lat'], row['stop_lon']], radius=5, color='red', fill=True, fill_color='blue', popup=name).add_to(ma_carte)

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
folium.Marker(gare_plus_proche, popup='Gare la plus proche', icon=folium.Icon(color='pink')).add_to(ma_carte)

#ajout de toutes les routes
data_frame_routes = pd.read_csv("data/routes.txt")
routes_stops = Routes_stops()#instance de Routes_stops
route_id_vect = data_frame_routes['route_id']
arret_route_vect = {}

for route_id in route_id_vect:
    if len(routes_stops.get_arret_routes(route_id))!=0:
        arret_route_vect[route_id] = routes_stops.get_arret_routes(route_id)






# Relier les arrêts par des lignes
for line_id , arret_route in arret_route_vect.items():
    for i in range(len(arret_route) - 1):
        print(arret_route)
        points = [(arret_route[i]["stop_lat"], arret_route[i]["stop_lon"]),
                (arret_route[i + 1]["stop_lat"], arret_route[i + 1]["stop_lon"])]
        folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(ma_carte)

#calcule du premier trajet qui relie 2 gares
id_gare_1 = "StopPoint:OCETrain TER-87723320"#venissieux
id_gare_2 = "StopPoint:OCETrain TER-87734475"

# Enregistrer la carte au format HTML
ma_carte.save('carte_auvergne_rhone_alpes.html')

#########