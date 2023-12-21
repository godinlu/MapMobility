import pandas as pd
from .region import Region
from .stops import Stops

class Routes_stops:
    """
    a remplir
    """
    def __init__(self, stop_path:str="data/stops.txt", stop_time_path:str="data/stop_times.txt",
                 trips_path:str="data/trips.txt", routes_path:str="data/routes.txt",) -> None:
        self.data_frame_stop = pd.read_csv(stop_path)
        self.data_frame_stop_time = pd.read_csv(stop_time_path)
        self.data_frame_trips = pd.read_csv(trips_path)
        self.data_frame_routes = pd.read_csv(routes_path)

    def get_arret_routes(self,self_route_id)->dict:
        """
        a remplir
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