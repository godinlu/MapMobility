from src.map import Map
from datetime import datetime

def main():
    map = Map('StopPoint:OCETrain TER-87761007', datetime(2024,4,2,20,0,0))
    map.add_gare()
    #map.add_trajet()
    map.save()

if __name__ == "__main__":
    main()