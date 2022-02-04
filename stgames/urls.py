"""stgames URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from stgame_recommend import views

urlpatterns = [
    # 관리자 페이지 url
    path('admin/', admin.site.urls),

    # 하위 앱 url파일 연결
    path('', include('stgame_recommend.urls')),

    # 시작 페이지 url
    path('', views.index, name='index'),

    # 로그인 url
    path('sign-in/', views.sign_in, name='sign-in'),

    # 회원가입 url
    path('sign-up/', views.sign_up, name='sign-up'),

    # 아이디 중복 확인 url
    path('id-check/', views.id_check, name='id-check'),

    # 이메일 중복 확인 url
    path('email-check/', views.email_check, name='email-check'),

    # 메인 페이지 url
    path('main/', views.main, name='main'),

    # 마이 페이지 url
    path('my-page/', views.my_page, name='my-page'),
]
