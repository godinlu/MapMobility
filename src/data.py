import pandas as pd
import json
import requests
import networkx as nx
from shapely.geometry import Point, Polygon,box
from src.stop_times_manager import StopTimesManager
from src.utils import meters_projection,haversine_distance,get_neighbors_indices,idx_to_row_col
import numpy as np
import geopandas as gpd
from tqdm import tqdm
import os


class Data:
    """
    Cette classe singleton sert à faire tous les imports de fichiers de données csv pour éviter 
    d'avoir plusieurs lecture de données à des endroits différents
    """
    _instance = None
    AURA_GRID_PATH = 'data/AURA_grid.json'

    @staticmethod
    def get_instance():
        if Data._instance is None:
            Data._instance = Data()
        return Data._instance
    
    def __init__(self) -> None:
        if Data._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to obtain an instance.")
        
        self._stops = pd.read_csv("data/stops.txt")
        self._stop_times = pd.read_csv("data/stop_times.txt")
        self._trips = pd.read_csv("data/trips.txt")
        self._routes = pd.read_csv("data/routes.txt")
        
        self._stop_times_manager = StopTimesManager()

        self._region_aura = gpd.read_file("data/region-auvergne-rhone-alpes.geojson")

        self.preprocess_data()

    def preprocess_data(self) -> None:
        """
        cette fonction enlèves les données superflue comme les bus et
        garde que les points de auvergne rhone alpes
        """
        #on commence par garder que les gare de trains
        self._stops = self._stops[self._stops['stop_id'].str.contains('Train')]

        #ensuite on garde que les gare qui sont dans auvergne rhâne alpes
        gdf_stops = gpd.GeoDataFrame(self._stops, geometry=gpd.points_from_xy(self._stops['stop_lon'], self._stops['stop_lat']))
        mask = gdf_stops.within(self._region_aura.geometry.unary_union)
        self._stops = self._stops[mask]

        #puis on garde que les trajet qui passent par les gares selectionné précédemment
        self._stop_times = self._stop_times[self._stop_times['stop_id'].isin(self._stops['stop_id'])]


    def get_grid_AURA(self) ->dict[str,list[list[float]]]:
        if not os.path.exists(self.AURA_GRID_PATH):
            self.create_grid_AURA()
        
        with open(self.AURA_GRID_PATH, "r") as json_file:
            return json.load(json_file) 

    
    def create_grid_AURA(self, length:int = 1000, height:int = 800) -> None:
        X_arr = np.linspace(self._region_aura.bounds.min()['minx'],self._region_aura.bounds.min()['maxx'],length)
        Y_arr = np.linspace(self._region_aura.bounds.min()['miny'],self._region_aura.bounds.min()['maxy'],height)

        with open('./data/region-auvergne-rhone-alpes.geojson') as f:
            geojson_data = json.load(f)
        region_polygon = Polygon(geojson_data['geometry']['coordinates'][0])

        aura_grid = {'3D':[], '2D':[]}
        for x in tqdm(X_arr):
            for y in Y_arr:
                if region_polygon.contains(Point(x,y)):
                    aura_grid['3D'].append((x,y))
                    aura_grid['2D'].append( meters_projection(x, y) )

        with open(self.AURA_GRID_PATH, "w") as file:
            json.dump(aura_grid, file)

    def get_graph_grid(self)->nx.graph:
        # Calculer les limites du GeoDataFrame
        minx, miny, maxx, maxy = self._region_aura.total_bounds
        # Définir les dimensions du quadrillage
        n_rows = 5
        n_cols = 5
        a = (maxx - minx) / n_cols  # Latitude
        b = (maxy - miny) / n_rows  # Longitude
        # Créer un GeoDataFrame pour le quadrillage
        grid = gpd.GeoDataFrame(geometry=gpd.GeoSeries([box(minx + i*a, miny + j*b, minx + (i+1)*a, miny + (j+1)*b) 
                                                        for j in range(n_rows) for i in range(n_cols)]))        
        # Initialiser une nouvelle colonne 'in_AURA' avec des valeurs par défaut à 0
        grid['in_AURA'] = 0
        # Filtrer les cellules du quadrillage qui intersectent la région AURA
        filtered_grid = gpd.overlay(grid, self._region_aura, how='intersection')
        # Marquer les cellules qui intersectent la région AURA avec 1
        for idx, row in filtered_grid.iterrows():
            grid_idx = grid.index[grid.intersects(row['geometry'])].tolist()
            grid.loc[grid_idx, 'in_AURA'] = 1
        # Calculer les centres des cellules filtrées
        centers = filtered_grid['geometry'].centroid
        # Convertir les points en tuples de coordonnées (longitude, latitude)
        coord_list = [(point.x, point.y) for point in centers]

        # Initialisation de grid_coords
        grid_coords = [[None for _ in range(n_cols)] for _ in range(n_rows)]
        a=0
        # Remplir le tableau 2D avec les coordonnées des centres
        for i in range(n_rows):
            for j in range(n_cols):
                if(a==0):
                    idx = i * n_cols + j
                else:
                    idx = i * n_cols + j + a
                if idx < len(coord_list):  # Vérifier que l'indice est dans la plage de coord_list
                    if grid.loc[i * n_cols + j, 'in_AURA'] == 1:
                        # Modifier les indices pour que (0,0) soit en bas à gauche
                        grid_coords[i][j] = coord_list[idx]
                    else:
                        grid_coords[i][j] = 0,0
                        a = a-1
                else:
                    grid_coords[i][j] = 0,0
        # Créer un graphe vide
        G = nx.Graph()
        # Ajouter chaque point de coord_list en tant que nœud au graphe
        for i, point in enumerate(coord_list):
            G.add_node(i, pos=point)
        # Ajouter des arêtes pour les voisins de chaque nœud
        for i in range(n_rows):
            for j in range(n_cols):
                idx = i * n_cols + j
                if grid.loc[idx, 'in_AURA'] == 1:
                    neighbors_indices = get_neighbors_indices(idx, n_rows, n_cols)

                    for neighbor_idx in neighbors_indices:
                        try:
                            # Vérifier si le voisin est également dans la région AURA
                            if grid.loc[neighbor_idx, 'in_AURA'] == 1:
                                G.add_edge(idx, neighbor_idx)
                        except IndexError:
                            # Gérer l'exception si l'index est hors de la plage
                            continue
        for edge in G.edges():
            
            start_point_idx = edge[0]
            end_point_idx = edge[1]

            start_row, start_col = idx_to_row_col(start_point_idx, n_cols)
            end_row, end_col = idx_to_row_col(end_point_idx, n_cols)
            
            start_point = [grid_coords[start_row][start_col][1], grid_coords[start_row][start_col][0]]  # Inverser la latitude et la longitude pour le point de départ
            end_point = [grid_coords[end_row][end_col][1], grid_coords[end_row][end_col][0]]  # Inverser la latitude et la longitude pour le point d'arrivée

        nb_err = 0
        # Ajouter les arêtes sur le graphe avec poids
        for edge in G.edges():
            start_point_idx = edge[0]
            end_point_idx = edge[1]

            start_row, start_col = idx_to_row_col(start_point_idx, n_cols)
            end_row, end_col = idx_to_row_col(end_point_idx, n_cols)
            
            start_point = [grid_coords[start_row][start_col][1], grid_coords[start_row][start_col][0]]  # Inverser la latitude et la longitude pour le point de départ
            end_point = [grid_coords[end_row][end_col][1], grid_coords[end_row][end_col][0]]  # Inverser la latitude et la longitude pour le point d'arrivée
            print(start_point,end_point)
            # Préparer le corps de la requête API
            body = {
                "coordinates": [
                    [start_point[1], start_point[0]],  # Inverser la latitude et la longitude
                    [end_point[1], end_point[0]]  # Inverser la latitude et la longitude
                ]
            }
            #print(body['coordinates'])
            headers = {
                'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
                'Authorization': '5b3ce3597851110001cf624880c449c8edfd422fa22fea1919286971',
                'Content-Type': 'application/json; charset=utf-8'
            }

            # Faire la requête API
            call = requests.post('https://api.openrouteservice.org/v2/directions/cycling-regular', json=body, headers=headers)
            response = call.text
            data = json.loads(response)
            
            try:
                duration = data['routes'][0]['summary']['duration']
                distance_app = haversine_distance(start_point[0],start_point[1],end_point[0],end_point[1])
                fly_speed = distance_app / duration *3.6
            except KeyError:
                fly_speed = 15
                nb_err = nb_err +1
            # Ajouter l'arête avec le poids de la durée
            G.add_edge(start_point_idx, end_point_idx, weight=fly_speed)
        return G


    def get_stops(self) -> pd.DataFrame:
        return self._stops
    
    def get_stop_times(self, weekday:int) -> pd.DataFrame:
        return self._stop_times_manager.get_stop_times(weekday)
    
    def get_trips(self) -> pd.DataFrame:
        return self._trips
    
    def get_routes(self) -> pd.DataFrame:
        return self._routes
    
    def get_aura(self) -> any:
        return self._region_aura