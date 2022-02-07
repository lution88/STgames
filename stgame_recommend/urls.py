from django.urls import path
from . import views

urlpatterns = [
    path('testurl/', views.take_url, name='takeurl'),
    path('tensorflow/', views.tensorflow, name='tensorflow')
]
