from django.shortcuts import render
from django.http import HttpResponse

from .forms import DateForm
from .backend.data import Data
from .backend.train_graph import TrainGraph
from .backend.time_grid import TimeGrid
from datetime import datetime




def index(request):
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            date = datetime.fromisoformat(form['date_field'].value())
    else:
        form = DateForm()
        date = datetime.now()

    gare_id = 'StopPoint:OCETrain TER-87723197'

    data = Data.get_instance()
    train_graph = TrainGraph(gare_id, date)
    time_grid = TimeGrid(train_graph.get_list_station())

    context = {
        'geo_json_aura' : data.get_aura().to_json(),
        'heatmap_data' : time_grid.get_grid(),
        'form':form
    }
    return render(request, "map/index.html",context)

