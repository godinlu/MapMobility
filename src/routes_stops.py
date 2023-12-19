import pandas as pd

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

    def get_arret_routes(self,routes)->pd.DataFrame:
        """
        a remplir
        """
        


        indexs = self.data_frame['stop_id'].str.contains('Train')
        colonnes_a_supprimer = ['stop_desc', 'zone_id','stop_url','location_type']
        return self.data_frame[indexs].drop(colonnes_a_supprimer, axis=1)

if __name__ == '__main__':

    routes_stops = Routes_stops()
    print(routes_stops.get_arret_routes())