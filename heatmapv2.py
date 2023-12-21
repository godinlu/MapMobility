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
import pandas as pd

centre = [45.75, 4.85]
carte = folium.Map(location=centre, zoom_start=7)
with open('./data/region-auvergne-rhone-alpes.geojson') as f:
    geojson_data = json.load(f)
zone_gpd = gpd.read_file("./data/region-auvergne-rhone-alpes.geojson")
folium.GeoJson(geojson_data).add_to(carte)

stops = Stops()
stops_data = stops.get_locations_train()
for index, row in stops_data.iterrows():
    if Region.is_in_region(row['stop_lat'], row['stop_lon']):
        name = row['stop_name']
        folium.CircleMarker([row['stop_lat'], row['stop_lon']], radius=5, color='red', fill=True, fill_color='blue', popup=name).add_to(carte)

data = pd.read_csv('./data/Distances_points_gares.csv')
data.drop('indexgare',axis=1,inplace = True)
heat_data = list(zip(data['lat'],data['long'],data['distance']))
#on crée la heatmap a partir du vecteur obtenu
HeatMap(heat_data,min_opacity=0.2,max_opacity = 0.3).add_to(carte)
#on sauvegarde la carte
carte.save('heatmap_distance_gare.html')