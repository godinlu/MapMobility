import folium

# Coordonnées centrales de la région Auvergne-Rhône-Alpes
latitude = 45.75
longitude = 4.85

# Créer la carte centrée sur la région
ma_carte = folium.Map(location=[latitude, longitude], zoom_start=7)

# Ajouter un marqueur pour indiquer le centre
folium.Marker([latitude, longitude], popup='Auvergne-Rhône-Alpes').add_to(ma_carte)

# Enregistrez la carte au format HTML
ma_carte.save('carte_auvergne_rhone_alpes.html')

#########