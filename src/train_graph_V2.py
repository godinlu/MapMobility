from .data import Data
import pandas as pd
from datetime import datetime, time

class TrainGraph:
    def __init__(self, gare_id:str, date:datetime) -> None:
        self.list_gare = {}
        self.df_stops_times = Data.get_instance().get_stops_times()
        self.df_stops_times = self.df_stops_times[
            self.df_stops_times['trip_id'].apply(lambda x: datetime.fromisoformat(x.split(':')[1]).weekday()) == date.weekday()
        ]

        #self.df_stops_times = 

        self.propagation(gare_id, date)



    def propagation(self, gare_id:str, date:datetime) -> None:
        #cas d'arret lorsqu'il existe un meilleur temps pour allé à la gare
        if (gare_id in self.list_gare and self.list_gare[gare_id] < date ):
            return;

        self.list_gare[gare_id] = date
        #cas simple de propagtion avec les autres gars
        
        self.get_next_stations(gare_id, date)

        #group = self.df_stops_times[self.df_stops_times['trip_id'].isin(stops_time['trip_id'])].groupby('trip_id')

        #on boucle dans les trips qui passe par la gare en question
        # for _, trip in group:
        #     gare_index = (trip['stop_id'] == gare_id)

        #     #on test si la gare en question n'est pas la dernière du trip
        #     if (len(trip) > gare_index+1):
        #         print()

    def get_next_stations(self, gare_id:str,  date:datetime):
        #trie sur la gare_id

        #trie sur l'heure
        index = self.df_stops_times['stop_id'] == gare_id & self.df_stops_times['departure_time'].apply(lambda x: time.fromisoformat(x)) > date.time()
 
        
        print(index)


    def to_datetime(string:str) -> datetime:



