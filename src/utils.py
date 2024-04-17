from math import radians, tan, log, pi, cos, sin
import math
from shapely.geometry import Point
import geopandas as gpd

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    cette fonction renvoie la distance en metres entre 2
    points
    """
    # Convertir les coordonnées de degrés à radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Calcul des différences de latitude et de longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Formule haversine
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Rayon de la Terre en mètres (approximatif)
    radius_earth = 6371000

    # Calcul de la distance
    distance = radius_earth * c

    return distance

def meters_projection(lat, lon) -> tuple[float, float]:
    return(lat*111000,lon*80000)

def heures_en_secondes(heure_str:str, sep:str=':')->int:
    """
    Cette fonction prend une heure par exemple '20:10:12' en entré 
    et renvoie l'équivalent en seconde
    """
    heures, minutes, secondes = map(int, heure_str.split(sep))
    return heures * 3600 + minutes * 60 + secondes

def get_bike_time_between(location1, location2,grid,avg_weights_grid)->int:
        """
        cette fonction prend 2 point sur la carte un point est représenté en [lattitude, longitude]
        puis renvoie le temps en minute du trajet à vélo.
        La fonction ne prend pas en compte les routes ou le dénivelé
        """
        case1,case2=test_case_grille(location1,location2,grid,avg_weights_grid)
        chemin = chemin_test(case1,case2)
        # Initialiser une liste pour stocker les vitesses de chaque case
        vitesses = []
        # Calculer la vitesse de chaque case dans le chemin
        for case in chemin:
            x, y = case
            vitesse = avg_weights_grid[x][y]  # Récupérer la vitesse de la case depuis avg_weights_grid
            vitesses.append(vitesse)
        # Calculer la vitesse moyenne
        vitesse_moyenne = sum(vitesses) / len(vitesses) if vitesses else 0
        dist = haversine_distance(location1[0],location1[1],location2[0],location2[1])
        time_s = dist/1000 / vitesse_moyenne*3600
        return time_s

def get_bike_time(distance:float)->int:
     """
     renvoie le temps en seconde de la distance en mètres à vélo en prenant 15km/h
     """
     return ((distance/1000) / 15 ) * 60 * 60

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

def chemin_test(case_1, case_2):
    chemin = []
    
    # Extraire les coordonnées de chaque case
    x1, y1 = case_1
    x2, y2 = case_2

    while x1 != x2 or y1 != y2:
        # Ajouter la case actuelle au chemin
        chemin.append((x1, y1))
        # Déplacer vers la prochaine case
        if x1 < x2:
            x1 += 1
        elif x1 > x2:
            x1 -= 1
        
        if y1 < y2:
            y1 += 1
        elif y1 > y2:
            y1 -= 1
    
    # Ajouter la dernière case au chemin
    chemin.append((x2, y2))
    
    return chemin

def test_case_grille(location_1, location_2,grid,avg_weights_grid):
     # Créer des Points à partir des coordonnées
    point_1 = Point(location_1[0], location_1[1])
    point_2 = Point(location_2[0], location_2[1])

    # Trouver la case correspondante pour location_1
    for i, row in grid.iterrows():
        if row['geometry'].contains(point_1):
            case_location_1 = (i // len(avg_weights_grid), i % len(avg_weights_grid))
            break

    # Trouver la case correspondante pour location_2
    for i, row in grid.iterrows():
        if row['geometry'].contains(point_2):
            case_location_2 = (i // len(avg_weights_grid), i % len(avg_weights_grid))
            break

    return case_location_1,case_location_2