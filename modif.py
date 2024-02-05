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
stops = Stops()
stops_data = stops.get_locations_train()
for index, row in stops_data.iterrows():
    if  not (Region.is_in_region(row['stop_lat'], row['stop_lon'])) :
        stops_data.drop(index,inplace=True)
data = pd.read_csv('./data/Distances_points_gares.csv')
data['indexgare'] = [stops_data.get(d, {}).get('stop_id') for (d) in  (data['indexgare'])]
data.to_csv('./data/Distances_points_gares.csv',index=False)

