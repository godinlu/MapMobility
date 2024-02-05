import geopandas as gpd
from shapely.geometry import Point

def point_dans_region_auvergne_rhone_alpes(latitude, longitude, fichier_geojson):
    # Charger le fichier GeoJSON de la région Auvergne-Rhône-Alpes
    region_auvergne_rhone_alpes = gpd.read_file(fichier_geojson)

    # Créer un objet Point avec les coordonnées du point
    point = Point(longitude, latitude)

    # Vérifier si le point est à l'intérieur de la région Auvergne-Rhône-Alpes
    est_dans_region = point.within(region_auvergne_rhone_alpes.geometry.iloc[0])

    return est_dans_region