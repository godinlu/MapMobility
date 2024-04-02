from .data import Data
import pandas as pd
from datetime import datetime, time, timedelta

class TrainGraph:
    def __init__(self, gare_id:str, date:datetime) -> None:
        self.list_gare = {}
        self.df_stops_times = Data.get_instance().get_stops_times()
        self.df_stops_times = self.df_stops_times[
            self.df_stops_times['trip_id'].apply(lambda x: datetime.fromisoformat(x.split(':')[1]).weekday()) == date.weekday()
        ]

        self.df_stops_times['date'] = self.df_stops_times['trip_id'].str.split(':').str[1].str[:-3]
        self.df_stops_times['departure_time'] = self.df_stops_times['date'] + ':' + self.df_stops_times['departure_time']
        self.df_stops_times['arrival_time'] = self.df_stops_times['date'] + ':' + self.df_stops_times['arrival_time']
        self.df_stops_times.drop(columns=['date'], inplace=True)

        for i, row in self.df_stops_times.iterrows():
            arr_hour = int(row['arrival_time'][11:13])
            if(arr_hour > 23):
                arrival_time = self.df_stops_times.at[i,'arrival_time']
                new_arrival_time = arrival_time[:11] + str(arr_hour - 24) + arrival_time[13:]
                self.df_stops_times.at[i,'arrival_time'] = new_arrival_time
                date = datetime.fromisoformat(self.df_stops_times['arrival_time']) + timedelta(days=1)
                self.df_stops_times.at[i,'arrival_time'] = date.strftime('%Y-%m-%d:%H:%M:%S')

            dep_hour = int(row['departure_time'][11:13])
            if(dep_hour > 23):
                departure_time = self.df_stops_times.at[i,'departure_time']
                new_departure_time = departure_time[:11] + str(arr_hour - 24) + departure_time[13:]
                self.df_stops_times.at[i,'departure_time'] = new_departure_time
                date = datetime.fromisoformat(self.df_stops_times['departure_time']) + timedelta(days=1)
                self.df_stops_times.at[i,'departure_time'] = date.strftime('%Y-%m-%d:%H:%M:%S')


        print(self.df_stops_times)
        #self.propagation(gare_id, date)

        print(TrainGraph.to_datetime('2024-03-12:24:13:00'))



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


    @staticmethod
    def to_datetime(date_str):
        # Convertir la chaîne de caractères en objet datetime
        if int(date_str[11:13]) > 23:
            date_str[11:13]
