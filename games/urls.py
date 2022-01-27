# tweet/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test, name='test'),  # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
   ]