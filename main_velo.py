import folium
import networkx as nx
import requests
import json
from src.data import Data
import geopandas as gpd
import numpy as np
from shapely.geometry import box, Point
from src.utils import haversine_distance
import time

# Convertir un indice unique en une paire d'indices (row, col)
def idx_to_row_col(idx, j):
    row = idx // j
    col = idx % j
    return row, col

def get_neighbors_indices(idx, i, j):
    """
    Trouve les indices des voisins d'un élément dans un vecteur de taille i*j.
    
    Args:
    - idx (int): Indice de l'élément dans le vecteur de taille i*j.
    - i (int): Nombre de lignes.
    - j (int): Nombre de colonnes.
    
    Returns:
    - list[int]: Liste des indices des voisins.
    """
    neighbors = []
    
    # Coordonnées de l'élément dans le tableau 2D
    row = idx // j
    col = idx % j
    
    # Indices des voisins
    offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    for di, dj in offsets:
        new_row, new_col = row + di, col + dj
        
        # Vérifier les limites du tableau
        if 0 <= new_row < i and 0 <= new_col < j:
            neighbors.append(new_row * j + new_col)
    
    return neighbors

data = Data()
AURA = data.get_instance().get_aura()
# Créer une carte centrée sur une certaine latitude et longitude
ma_carte = folium.Map(location=[45.75, 4.85], zoom_start=7)

folium.GeoJson(AURA).add_to(ma_carte)


# Calculer les limites du GeoDataFrame
minx, miny, maxx, maxy = AURA.total_bounds

# Définir les dimensions du quadrillage
n_rows = 4
n_cols = 4
a = (maxx - minx) / n_cols  # Latitude
b = (maxy - miny) / n_rows  # Longitude

# Créer un GeoDataFrame pour le quadrillage
grid = gpd.GeoDataFrame(geometry=gpd.GeoSeries([box(minx + i*a, miny + j*b, minx + (i+1)*a, miny + (j+1)*b) 
                                                for j in range(n_rows) for i in range(n_cols)]))

# Ajouter les limites du quadrillage au folium
for _, row in grid.iterrows():
    bounds = row['geometry'].bounds
    folium.Rectangle(
        bounds=[(bounds[1], bounds[0]), (bounds[3], bounds[2])],
        color='blue',
        fill=True,
        fill_opacity=0.2
    ).add_to(ma_carte)


# Initialiser une nouvelle colonne 'in_AURA' avec des valeurs par défaut à 0
grid['in_AURA'] = 0
# Filtrer les cellules du quadrillage qui intersectent la région AURA
filtered_grid = gpd.overlay(grid, AURA, how='intersection')



# Marquer les cellules qui intersectent la région AURA avec 1
for idx, row in filtered_grid.iterrows():
    grid_idx = grid.index[grid.intersects(row['geometry'])].tolist()
    grid.loc[grid_idx, 'in_AURA'] = 1


# Calculer les centres des cellules filtrées
centers = filtered_grid['geometry'].centroid
# Ajouter les centres des cellules filtrées à la carte
for idx, center in centers.items():  # Utilise `items()` au lieu de `iteritems()`
    folium.Marker([center.y, center.x],  # Latitude et Longitude du centre
                  popup=f"Centre {center.y, center.x}").add_to(ma_carte)
    

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
#print(grid_coords)
# Afficher la liste de coordonnées
#print(coord_list)

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
                    #print(IndexError)
                    continue



#print(len(coord_list))

#print(G.number_of_edges())


#print(grid_coords)
# Ajouter les arêtes sur la carte
for edge in G.edges():
    
    start_point_idx = edge[0]
    end_point_idx = edge[1]

    start_row, start_col = idx_to_row_col(start_point_idx, n_cols)
    end_row, end_col = idx_to_row_col(end_point_idx, n_cols)
    
    start_point = [grid_coords[start_row][start_col][1], grid_coords[start_row][start_col][0]]  # Inverser la latitude et la longitude pour le point de départ
    end_point = [grid_coords[end_row][end_col][1], grid_coords[end_row][end_col][0]]  # Inverser la latitude et la longitude pour le point d'arrivée
    #print("xa ", start_point)
    #print("xb ", end_point)
    folium.PolyLine(locations=[start_point, end_point], color='red').add_to(ma_carte)



nb_err = 0
# Ajouter les arêtes sur le graphe avec poids
for edge in G.edges():
    start_point_idx = edge[0]
    end_point_idx = edge[1]

    start_row, start_col = idx_to_row_col(start_point_idx, n_cols)
    end_row, end_col = idx_to_row_col(end_point_idx, n_cols)
    
    start_point = [grid_coords[start_row][start_col][1], grid_coords[start_row][start_col][0]]  # Inverser la latitude et la longitude pour le point de départ
    end_point = [grid_coords[end_row][end_col][1], grid_coords[end_row][end_col][0]]  # Inverser la latitude et la longitude pour le point d'arrivée
    #print(start_point,end_point)
    # Préparer le corps de la requête API
    body = {
        "coordinates": [
            [start_point[1], start_point[0]],  # Inverser la latitude et la longitude
            [end_point[1], end_point[0]]  # Inverser la latitude et la longitude
        ],
        "radiuses": [-1, -1]
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
    print(data)
    
    try:
        duration = data['routes'][0]['summary']['duration']
        distance_app = haversine_distance(start_point[0],start_point[1],end_point[0],end_point[1])
        fly_speed = distance_app / duration *3.6
    except KeyError:
        fly_speed = 15
        nb_err = nb_err +1
    # Ajouter l'arête avec le poids de la durée
    G.add_edge(start_point_idx, end_point_idx, weight=fly_speed)
    time.sleep(3)
    
    folium.PolyLine(locations=[start_point, end_point], color='red',popup=f" {fly_speed} km/h").add_to(ma_carte)
print(nb_err)
# Afficher la carte
ma_carte.save("ma_carte.html")