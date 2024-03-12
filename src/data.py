import pandas as pd

class Data:
    """
    Cette classe singleton sert à faire tous les imports de fichiers de données csv pour éviter 
    d'avoir plusieurs lecture de données à des endroits différents
    """
    _instance = None

    @staticmethod
    def get_instance():
        if Data._instance is None:
            Data._instance = Data()
        return Data._instance
    
    def __init__(self) -> None:
        if Data._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to obtain an instance.")
        
        self._stops = pd.read_csv("data/stops.txt")
        self._stop_times = pd.read_csv("data/stop_times.txt")
        self._trips = pd.read_csv("data/trips.txt")
        self._calendar_dates = pd.read_csv("data/calendar_dates.txt")
        self._routes = pd.read_csv("data/routes.txt")

    def get_stops(self) -> pd.DataFrame:
        return self._stops
    
    def get_stops_times(self) -> pd.DataFrame:
        return self._stop_times
    
    def get_trips(self) -> pd.DataFrame:
        return self._trips
    
    def get_calendar_dates(self) -> pd.DataFrame:
        return self._calendar_dates
    
    def get_routes(self) -> pd.DataFrame:
        return self._routes