from django.shortcuts import render
from django.http import HttpResponse

from .forms import mapForm
from .backend.data import Data
from .backend.train_graph import TrainGraph
from .backend.time_grid import TimeGrid
from datetime import datetime




def index(request):
    if request.method == "POST":
        form = mapForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date_field']
            lat, lng = form.cleaned_data['lattitude'], form.cleaned_data['longitude']
    else:
        date = datetime.now()
        lat, lng = 45.7640, 4.8357
        form = mapForm(initial={
            "date_field":date,
            "lattitude":lat,
            "longitude":lng
        })
        
        

    gare_id = 'StopPoint:OCETrain TER-87723197'
    data = Data.get_instance()
    train_graph = TrainGraph(gare_id, date)
    time_grid = TimeGrid(train_graph.get_list_station())

    context = {
        'geo_json_aura' : data.get_aura().to_json(),
        'heatmap_data' : time_grid.get_grid(),
        'start_coord' : [lat, lng],
        'form':form
    }
    return render(request, "map/index.html",context)

