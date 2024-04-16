//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//          VARIABLE GLOBALE
let map = L.map('map').setView([45.75, 4.85], 7);
let lattitude = document.getElementById("id_lattitude")
let longitude = document.getElementById("id_longitude")


//////////////////////////////////////////////////////////////////////////////////////////////////////////////

function time_in_str(secondes) {
    var heures = Math.floor(secondes / 3600);
    var minutes = Math.floor((secondes % 3600) / 60);
    return heures + "h" + minutes;
}

function find_time(points, targetLatLng) {
    var nearestPoint = null;
    var minDistanceSquared = Infinity;

    // Parcourir tous les points dans le tableau
    for (var i = 0; i < points.length; i++) {
        var point = points[i];
        var lat = point[0];
        var lng = point[1];

        // Calculer la distance euclidienne (squared) entre le point actuel et la LatLng cible
        var distanceSquared = Math.pow(lat - targetLatLng.lat, 2) + Math.pow(lng - targetLatLng.lng, 2);

        // Mettre à jour le point le plus proche si la distance actuelle est plus petite
        if (distanceSquared < minDistanceSquared) {
            minDistanceSquared = distanceSquared;
            nearestPoint = point;
        }
    }

    return time_in_str(nearestPoint[2]);
} 

function click_handler(event){
    // Récupérer les coordonnées du clic
    var latlng = event.latlng;

    // Afficher la valeur dans une fenêtre contextuelle
    L.popup()
        .setLatLng(latlng)
        .setContent("" + find_time(heat_data,latlng))
        .openOn(map);
}

function on_move_handler(event){
    const latlng = event.latlng;
    lattitude.value = latlng.lat
    longitude.value = latlng.lng
}

function handle_click_choose_loc(event){

    map.on('mousemove', on_move_handler);
    map.off('click', click_handler);
    map.on('click', function(e){
        map.off('mousemove', on_move_handler);
    });
}




function init_heatmap(heatmap_data, gdf_aura, start_coord){

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

    L.geoJSON(gdf_aura).addTo(map);

    // Ajouter la heatmap à partir des données transmises
    L.heatLayer(heatmap_data, {
        "blur": 15, 
        "max" : 1,
        "maxOpacity": 0.3, 
        "maxZoom": 18, 
        "minOpacity": 0.2, 
        "radius": 15,
        "gradient": {
                0.3: 'blue',
                0.5: 'lime',
                0.6: 'yellow',
                0.8: 'orange',
                0.9: 'red',
                0.95: 'darkred'
            }
    }).addTo(map);

    map.on('click', click_handler);
    L.marker(start_coord).addTo(map)

}





function main(){
    document.getElementById('choose_loc').addEventListener("click", handle_click_choose_loc)
}
main()

