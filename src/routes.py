import pandas as pd
import os

class Routes:
    TRAIN_ROUTES_ID_PATH = 'data/train_routes_id.csv'


    @staticmethod
    def get_train_id()->pd.DataFrame:
        """
        cette fonction renvoie tous les id des routes qui sont un train
        lorsque la fonction est appelé pour la première fois elle créer un fichier train_routes_id.csv
        pour que lorsqu'elle soit rappelé elle ne refasse pas tout le calcul
        """
        if (not os.path.exists(Routes.TRAIN_ROUTES_ID_PATH)):
            #ici on est dans le cas ou il faut créer le fichier train_routes_id.csv
            stop_times = pd.read_csv('data/stop_times.txt')
            trips = pd.read_csv('data/trips.txt')

            stop_times = stop_times[stop_times['stop_id'].str.contains('Train')]
            stop_times.drop_duplicates(subset='trip_id', inplace=True)
            link = pd.merge(trips, stop_times, left_on='trip_id', right_on='trip_id', how='inner')
            link.drop_duplicates(subset='route_id', inplace=True)

            link[['route_id']].to_csv(Routes.TRAIN_ROUTES_ID_PATH, index=False)

        return pd.read_csv(Routes.TRAIN_ROUTES_ID_PATH)
            

            


if __name__ == '__main__':
    print(Routes.get_train_id())
