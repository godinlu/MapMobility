import requests
import json
from src.utils import haversine_distance


coor_gre = [4.8343, 45.7690]
coor_lyon = [5.7218, 45.1905]
coor_massif_centrale = [2.9083,45.4800]
coor_Saint_elouen_mine = [2.7618,46.0927]

body = {
    "coordinates": [
        coor_massif_centrale,
        coor_gre
    ]
}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf624880c449c8edfd422fa22fea1919286971',
    'Content-Type': 'application/json; charset=utf-8'
}

call = requests.post('https://api.openrouteservice.org/v2/directions/cycling-regular', json=body, headers=headers)

# Supposons que 'response' contient la réponse de la requête
response = call.text

# Convertir la réponse en JSON
data = json.loads(response)

# Récupérer la durée à partir des données JSON
duration = data['routes'][0]['summary']['duration']


distance_app = haversine_distance(46.0927,2.7618,45.7690,4.8343)

print("vitesse à vol d'oiseau du trajet :", duration, "en seconde")