import folium
import json
import geopandas as gpd
import pandas as pd
from folium.plugins import HeatMap
from shapely.geometry import Point, Polygon
import numpy as np
from tqdm import tqdm
from src.routes_stops import Routes_stops
from src.stops import Stops
from scipy.spatial import KDTree
from src.region import Region
from shapely.ops import unary_union
from main import trouver_chemin_entre_deux_gares
import os

centre = [45.75, 4.85]
carte = folium.Map(location=centre, zoom_start=7)
with open('./data/region-auvergne-rhone-alpes.geojson') as f:
    geojson_data = json.load(f)
zone_gpd = gpd.read_file("./data/region-auvergne-rhone-alpes.geojson")
folium.GeoJson(geojson_data).add_to(carte)


stops = Stops()
stops_data = stops.get_locations_train()
for index, row in stops_data.iterrows():
    name = row['stop_name']
    folium.CircleMarker([row['stop_lat'], row['stop_lon']], radius=5, color='red', fill=True, fill_color='blue', popup=name).add_to(carte)


data = pd.read_csv('./data/Distances_points_gares.csv')


point = (44.95526070591957,2.1090463874917345)
points_gares = list(zip(stops_data['stop_lat'], stops_data['stop_lon']))
kdtree_328 = KDTree(points_gares)
distpoint, garepoint = kdtree_328.query(point)
stops_data.index = range(len(stops_data))
garepoint = stops_data['stop_id'][int(garepoint)]

data['tps'] = None
for index, row in data.iterrows():
    chemin = trouver_chemin_entre_deux_gares(row['indexgare'],garepoint) 
    if (chemin):
        row['tempspoint'] = distpoint + dist_chem + row['distance'] #a modifier pour avoir la distance du chemin 
    else:   
        x = 0#je sais pas encore


