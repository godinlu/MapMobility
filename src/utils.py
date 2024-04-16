from math import radians, tan, log, pi, cos, sin
import math

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

def get_bike_time_between(location1, location2)->int:
        """
        cette fonction prend 2 point sur la carte un point est représenté en [lattitude, longitude]
        puis renvoie le temps en minute du trajet à vélo.
        La fonction ne prend pas en compte les routes ou le dénivelé
        """
        #on calcul la distance en mettres
        x1, y1 = location1[0]*111000, location1[1]*80000
        x2, y2 = location2[0]*111000, location2[1]*80000
        metres = math.sqrt((x1-x2)**2 + (y1-y2)**2)

        #ensuite on calcul le temps en prenant 15km/h
        return ((metres/1000) / 15 ) * 60 * 60

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
