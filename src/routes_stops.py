import pandas as pd
from .region import Region
from .stops import Stops
from .data import Data

class Routes_stops:
    """
    a remplir
    """
    def __init__(self) -> None:
        
        data = Data.get_instance()
        self.data_frame_stop = data.get_stops() 
        self.data_frame_stop_time = data.get_stops_times() 
        self.data_frame_trips = data.get_trips()
        self.data_frame_routes = data.get_routes()


    def get_arret_routes(self,self_route_id)->dict:
        """
        Cette fonction renvoit les arrets d'une route. 
        Elle renvoit un dictionnaire qui contient le stop_id, la stop_lat et la stop_lon pour chaque arrêt de la ligne.
        """
        trip_ide = self.data_frame_trips[self.data_frame_trips["route_id"] == self_route_id]['trip_id'].iloc[0]
        stop_ides = self.data_frame_stop_time[self.data_frame_stop_time["trip_id"] == trip_ide]['stop_id']
        stops = []
        
        for stop_ide in stop_ides:
            stop_data = self.data_frame_stop[self.data_frame_stop["stop_id"] == stop_ide][['stop_id','stop_lat', 'stop_lon']]
            if Region.is_in_region(stop_data['stop_lat'], stop_data['stop_lon']):
                stop_dict = stop_data.set_index('stop_id').to_dict(orient='index')
                stop_dict[stop_ide]['stop_id'] = stop_ide
                stops.append(stop_dict[stop_ide])
            #stop_dict = stop_data.set_index('stop_id').to_dict(orient='index')
            #stop_dict[stop_ide]['stop_id'] = stop_ide
            #stops.append(stop_dict[stop_ide])

        return stops

        # Maintenant, route_stops contient une liste des arrêts avec leurs coordonnées pour chaque route_ide

        # for route_ide in self.data_frame_routes['route_id']:
        #     trip_ide = self.data_frame_trips[self.data_frame_trips["route_id"] == route_ide]['trip_id'].iloc[0]
        #     stop_ides = self.data_frame_stop_time[self.data_frame_stop_time["trip_id"] == trip_ide]['stop_id']
        #     for stop_ide in stop_ides:
        #         coord = self.data_frame_stop[self.data_frame_stop["stop_id"] == stop_ide][['stop_id','stop_lat', 'stop_lon']]
                
        # return coord


if __name__ == '__main__':

    routes_stops = Routes_stops()
    route_id = 'FR:Line::05C666F4-3B26-4DB6-A4A8-F3C6D6150B76:'
    print(routes_stops.get_arret_routes(route_id))