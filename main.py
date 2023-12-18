import folium
import json
# Coordonnées centrales de la région Auvergne-Rhône-Alpes
points = [
    {"name": "Lyon", "location": [45.75, 4.85]},
    {"name": "Clermont-Ferrand", "location": [45.78, 3.08]},
    {"name": "Grenoble", "location": [45.19, 5.72]},
    # Ajoutez d'autres points avec leurs coordonnées ici
]

# Créer la carte centrée sur la région
ma_carte = folium.Map(location=[45.75, 4.85], zoom_start=7)

# Ajouter un marqueur pour indiquer le centre
folium.Marker([45.75, 4.85], popup='Auvergne-Rhône-Alpes').add_to(ma_carte)
# Ajouter un marqueur pour chaque point
for point in points:
    name = point["name"]
    location = point["location"]
    folium.CircleMarker(location, radius=5, color='red', fill=True, fill_color='blue', popup=name).add_to(ma_carte)
# Charger le fichier GeoJSON des frontières de la région
with open('./region-auvergne-rhone-alpes.geojson') as f:
    geojson_data = json.load(f)

# Ajouter le GeoJSON à la carte pour afficher les contours de la région
folium.GeoJson(geojson_data).add_to(ma_carte)

# Enregistrer la carte au format HTML
ma_carte.save('carte_auvergne_rhone_alpes.html')

#########