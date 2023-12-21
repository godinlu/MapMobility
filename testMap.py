from src.utils import get_bike_time
from src.routes_stops import Routes_stops

routes_stops = Routes_stops()
route_id = 'FR:Line::05C666F4-3B26-4DB6-A4A8-F3C6D6150B76:'
print(routes_stops.get_arret_routes(route_id))

coord1 = (45.77671, 3.08819)  # Coordonnées de Paris, France
coord2 = (44.19582, 5.72788)  # Coordonnées de Londres, Royaume-Uni
print(get_bike_time(coord1, coord2) /60)
#aura.save()