import folium
from .region import Region

class Map:
    def __init__(self, location=[45.75, 4.85], zoom_start=7) -> None:
        #on créer un instance d'une carte folium
        self.carte = folium.Map(location=[45.75, 4.85], zoom_start=7)

        #on dessine les contour de la region auvergne rhônes alpes
        folium.GeoJson(Region.get_geo_json()).add_to(self.carte)

    
    def save(self)->None:
        self.carte.save('carte_auvergne_rhone_alpes.html')
