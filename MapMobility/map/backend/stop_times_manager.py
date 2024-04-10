import os
import pandas as pd
import geopandas as gpd
from MapMobility.settings import PATH_IN, PATH_DAYS, PATH_SCORE
import json
from datetime import date

class StopTimesManager:
    """
    Cette classe permet de gérer les stop_times pour :
    - avoir chaque jours de la semaine avec le plus de données
    - update les jours de la semaine pour avec de meilleurs données
    - si un fichier stop_times.txt se trouve dans le fichier data/stop_times/in alors il sera traiter
    """

    def __init__(self) -> None:
        with open(PATH_SCORE, "r") as json_file:
            self.days_score = json.load(json_file)

        for file in os.listdir(PATH_IN):
            if file.endswith(".txt"):
                file_path = os.path.join(PATH_IN, file)
                if os.path.isfile(file_path):
                    self.check_files(file_path)
                else:
                    print(f"Le chemin {file_path} n'est pas un fichier valide.")

        with open(PATH_SCORE, "w") as json_file:
            json.dump(self.days_score, json_file)


    def check_files(self, file_path:str) -> pd.DataFrame:
        stop_time = pd.read_csv(file_path)
        required_keys = ["trip_id","arrival_time","departure_time","stop_id","stop_sequence","stop_headsign","pickup_type","drop_off_type","shape_dist_traveled"]

        if all(key in stop_time.columns for key in required_keys):
            print("Le fichier : ", file_path, " en cours de traitement")
            self.maj_score(stop_time)
            print("Le fichier : ", file_path, " a été correctement traité et supprimé")
            os.remove(file_path)
        else:
            os.remove(file_path)
            print("Le fichier : ", file_path, " n'est pas valide il a donc été supprimé")

    def maj_score(self, df:pd.DataFrame):
        df = self.preprocess_data(df)
        df['date'] = df['trip_id'].str.split(':').str[1].str[:-3]
        for group_name, group in df.groupby('date'):
            weekday = str(date.fromisoformat(group_name).weekday())

            if group.shape[0] > self.days_score[weekday]:
                name = "stop_times_" + weekday + ".txt"
                print("le fichier ", name, " a été mis à jour. Le score est passé de ",
                      self.days_score[weekday], " à ", group.shape[0])
                group.to_csv(os.path.join(PATH_DAYS, name), sep="\t", index=False)
                self.days_score[weekday] = group.shape[0]

    def preprocess_data(self, df:pd.DataFrame):
        region_aura = gpd.read_file("data/region-auvergne-rhone-alpes.geojson")
        stops = pd.read_csv("data/stops.txt")
        stops = stops[stops['stop_id'].str.contains('Train')]
        gdf_stops = gpd.GeoDataFrame(stops, geometry=gpd.points_from_xy(stops['stop_lon'], stops['stop_lat']))
        mask = gdf_stops.within(region_aura.geometry.unary_union)
        df = df[df['stop_id'].isin(stops[mask]['stop_id'])]
        return df

    def get_stop_times(self, weekday:int)->pd.DataFrame:
        name = "stop_times_" + str(weekday) + ".txt"
        return pd.read_csv(os.path.join(PATH_DAYS, name), sep="\t")