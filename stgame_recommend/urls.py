from django.urls import path
from . import views

urlpatterns = [
    path('testurl/', views.take_url, name='takeurl'),
    path('tensorflow/', views.tensorflow, name='tensorflow'),
    path('test2/', views.test2, name='test2'),
    path('mypage/', views.mypage, name='test'),
]
