import folium
import json
import geopandas as gpd
from folium.plugins import HeatMap
from shapely.geometry import Point, Polygon
import numpy as np

#on crée la carte de base, et on récupère le json
centre = [45.75, 4.85]
carte = folium.Map(location=centre, zoom_start=7)
with open('./region-auvergne-rhone-alpes.geojson') as f:
    geojson_data = json.load(f)
folium.GeoJson(geojson_data).add_to(carte)
zone_gpd = gpd.read_file("region-auvergne-rhone-alpes.geojson")

#on transforme le json en objet polygon
region_polygon = Polygon(geojson_data['geometry']['coordinates'][0])
#on récupère les points des coins du plus petit rectangle contenant la zone définie par le json
minx = zone_gpd.bounds.min()['minx']
miny = zone_gpd.bounds.min()['miny']
maxx = zone_gpd.bounds.min()['maxx']
maxy = zone_gpd.bounds.min()['maxy']
#on réparti des points de manière équidistants dans le rectangle
arrayx = np.linspace(minx,maxx,100)
arrayy = np.linspace(miny,maxy,100)
#on définie la fonction definissant la couleure de la heatmap
def rdmfonction(x, y):
    return np.sqrt((centre[0]-y)**2 +(centre[1]-x)**2)
#on crée le vecteur heat_data qui va contenir les données de la heatmap
heat_data = []
#pour chaque points du rectangle, si celui-ci est contenu dans la région voulu, on ajoute au vecteur heat_data les coordonnées du point,
#ainsi que sa valeur par la fonction rdmfonction
for x in arrayx:
    for y in arrayy:
        point = Point(x,y)
        if region_polygon.contains(point):
            heat_data.append((y,x,rdmfonction(x,y)))
#on affiche le vecteur ainsi crée
print(heat_data)
#on crée la heatmap a partir du vecteur obtenu
HeatMap(heat_data,min_opacity=0.2,max_opacity = 0.3).add_to(carte)

#on sauvegarde la carte
carte.save('heatmap_test.html')