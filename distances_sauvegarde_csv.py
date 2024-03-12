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

with open('./data/region-auvergne-rhone-alpes.geojson') as f:
    geojson_data = json.load(f)
zone_gpd = gpd.read_file("./data/region-auvergne-rhone-alpes.geojson")
#on transforme le json en objet polygon
region_polygon = Polygon(geojson_data['geometry']['coordinates'][0])
#on récupère les points des coins du plus petit rectangle contenant la zone définie par le json
minx = zone_gpd.bounds.min()['minx']
miny = zone_gpd.bounds.min()['miny']
maxx = zone_gpd.bounds.min()['maxx']
maxy = zone_gpd.bounds.min()['maxy']
#on réparti des points de manière équidistants dans le rectangle
arraylong = np.linspace(minx,maxx,1000)
arraylat = np.linspace(miny,maxy,1000)
region_polygon = unary_union(region_polygon.simplify(tolerance=0.001))

stops = Stops()
stops_data = stops.get_locations_train()
"""""
for index, row in stops_data.iterrows():
    if  not (Region.is_in_region(row['stop_lat'], row['stop_lon'])) :
        stops_data.drop(index,inplace=True)
"""

""" def mindist(lat,long):
    mindist = 100000
    minindx = 0
    indexx = 0
    for index, row in stops_data.iterrows():
        dist = np.sqrt((long-row['stop_lon'])**2 + (lat-row['stop_lat'])**2)
        if dist < mindist :
            mindist = dist
            minindx = indexx
        indexx = indexx + 1
    return((mindist,minindx)) """


liste_points = []
for x in tqdm(arraylong):
    for y in arraylat:
        point = Point(x,y)
        #dist = mindist(y,x)
        if region_polygon.contains(point):
            liste_points.append((y,x))



points_gares = list(zip(stops_data['stop_lat'], stops_data['stop_lon']))
stops_data.index = range(len(stops_data))
kdtree_328 = KDTree(points_gares)
distances, indices = kdtree_328.query(np.array(liste_points))
res =  [(a, b, c, stops_data['stop_id'][int(d)]) for (a, b), c, d in zip(liste_points, distances, indices)]
resdf = pd.DataFrame(   res,columns=['lat','long','distance','indexgare'])
resdf.to_csv('./data/Distances_points_gares.csv',index=False)

