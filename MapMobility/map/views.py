from django.shortcuts import render
from django.http import HttpResponse
from .backend.data import Data


def index(request):
    data = Data.get_instance()

    context = {
        'geo_json_aura' : data.get_aura().to_json()
    }
    return render(request, "map/index.html",context)

