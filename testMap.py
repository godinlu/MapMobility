from src.utils import get_bike_time

coord1 = (45.77671, 3.08819)  # Coordonnées de Paris, France
coord2 = (44.19582, 5.72788)  # Coordonnées de Londres, Royaume-Uni
print(get_bike_time(coord1, coord2) /60)
#aura.save()