import os
import pandas as pd
import json
from datetime import date

class StopTimesManager:
    IN_PATH = 'data/stop_times/in'
    DAYS_PATH = 'data/stop_times/days'
    SCORE_PATH = 'data/stop_times/days/days_score.json'
    """
    Cette classe permet de gérer les stop_times pour :
    - avoir chaque jours de la semaine avec le plus de données
    - update les jours de la semaine pour avec de meilleurs données
    - si un fichier stop_times.txt se trouve dans le fichier data/stop_times/in alors il sera traiter
    """

    def __init__(self) -> None:
        with open(StopTimesManager.SCORE_PATH, "r") as json_file:
            self.days_score = json.load(json_file)

        for file in os.listdir(StopTimesManager.IN_PATH):
            if file.endswith(".txt"):
                file_path = os.path.join(StopTimesManager.IN_PATH, file)
                if os.path.isfile(file_path):
                    self.check_files(file_path)
                else:
                    print(f"Le chemin {file_path} n'est pas un fichier valide.")

        with open(StopTimesManager.SCORE_PATH, "w") as json_file:
            json.dump(self.days_score, json_file)


    def check_files(self, file_path:str) -> pd.DataFrame:
        stop_time = pd.read_csv(file_path)
        required_keys = ["trip_id","arrival_time","departure_time","stop_id","stop_sequence","stop_headsign","pickup_type","drop_off_type","shape_dist_traveled"]

        if all(key in stop_time.columns for key in required_keys):
            print("Le fichier : ", file_path, " en cours de traitement")
            self.maj_score(stop_time)
        else:
            os.remove(file_path)
            print("Le fichier : ", file_path, " n'est pas valide il a donc été supprimé")

    def maj_score(self, df:pd.DataFrame):
        df['date'] = df['trip_id'].str.split(':').str[1].str[:-3]
        for group_name, group in df.groupby('date'):
            weekday = date.fromisoformat(group_name).weekday()

            if group.shape[0] > self.days_score[weekday]:
                name = "stop_times_" + weekday + ".txt"
                df.to_csv(os.path.join(self.DAYS_PATH, name), sep="\t", index=False)
                self.days_score[weekday] = group.shape[0]
