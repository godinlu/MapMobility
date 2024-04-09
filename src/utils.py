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

def get_bike_time(location1, location2)->int:
        """
        cette fonction prend 2 point sur la carte un point est représenté en [lattitude, longitude]
        puis renvoie le temps en minute du trajet à vélo.
        La fonction ne prend pas en compte les routes ou le dénivelé
        """
        #on calcul la distance en mettres
        metres = haversine_distance(location1[0],location1[1], location2[0], location2[1])

        #ensuite on calcul le temps en prenant 15km/h
        return ((metres/1000) / 15 ) * 60

def get_bike_time(distance:float)->int:
     """
     renvoie le temps en seconde de la distance à vélo en prenant 15km/h
     """
     return ((distance/1000) / 15 ) * 60 * 60