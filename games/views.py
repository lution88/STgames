from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import Games
import pandas as pd
import csv

# Create your views here.
def test(request):
    with open('test.csv') as file:
        s = csv.DictReader(file)
        s = pd.DataFrame(s)

    print()

    ls = []
    for i in list(s['GameName']):
        ls.append(Games(game=f'{i}'))
    print(ls)
    Games.objects.bulk_create(ls)
    return render(request, 'test.html', )
