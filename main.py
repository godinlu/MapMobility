from src.map import Map

def main():
    map = Map()
    map.add_gare()
    map.add_trajet()
    map.save()

if __name__ == "__main__":
    main()