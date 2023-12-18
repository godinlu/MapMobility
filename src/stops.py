import pandas as pd

class Stops:
    """
    Cette classe sert à tous les traitement de données correspondant au fichier stops.txt
    """
    def __init__(self, path:str="data/stops.txt") -> None:
        self.data_frame = pd.read_csv(path)

    def get_locations_train(self)->pd.DataFrame:
        """
        Cette fonction renvoie un dataframe contenant:
        stop_id, stop_name, stop_lat, stop_lon, parent_station
        de toute les gare de train
        """
        indexs = self.data_frame['stop_id'].str.contains('Train')
        colonnes_a_supprimer = ['stop_desc', 'zone_id','stop_url','location_type']
        return self.data_frame[indexs].drop(colonnes_a_supprimer, axis=1)

if __name__ == '__main__':

    stops = Stops()
    print(stops.get_locations_train())