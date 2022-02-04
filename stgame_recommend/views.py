from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import re

from .models import UserModel
from django.contrib import messages


# 시작 페이지(로그인 및 회원가입)
def index(request):
    return render(request, 'sign_in_and_up.html')


# 로그인
def sign_in(request):
    if request.method == 'POST':
        user_id = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=user_id, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/main')
        else:
            messages.error(request, '아이디나 비밀번호를 확인해 주세요!')
            return render(request, 'sign_in_and_up.html')

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/main')
        else:
            return render(request, 'sign_in_and_up.html')


# 회원가입
def sign_up(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/main')
        else:
            return render(request, 'sign_in_and_up.html')

    elif request.method == 'POST':
        user_id = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        nickname = request.POST.get('nickname', '')
        email = request.POST.get('email', '')

        if password != password2:
            return render(request, 'sign_in_and_up.html', {'error': '비밀번호가 다릅니다!'})
        else:
            if user_id == '' or password == '' or nickname == '' or email == '':
                return render(request, 'sign_in_and_up.html', {'error': '빈칸은 모두 채워 주세요!'})

            exist_user = UserModel.objects.filter(username=user_id) or UserModel.objects.filter(email=email)
            if exist_user:
                return render(request, 'sign_in_and_up.html', {'error': '해당 아이디나 이메일이 사용 중입니다. 중복확인 먼저 해 주세요!'})
            else:
                UserModel.objects.create_user(username=user_id, password=password, nickname=nickname, email=email)
                return render(request, 'sign_in_and_up.html')


# 메인 페이지(게임 추천)
@csrf_exempt
@login_required
def main(request):
    return render(request, 'main.html')


# 마이 페이지(로그인 한 유저 정보)
@csrf_exempt
@login_required
def my_page(request):
    return render(request, 'my_page.html')


# 로그아웃
@csrf_exempt
@login_required  # 사용자가 로그인 꼭 되어있어야 접근 가능함 표시
def logout(request):
    auth.logout(request)
    return redirect('')


# 아이디 중복 확인 및 유효성 검사
@csrf_exempt
def id_check(request):
    if request.method == 'POST':
        user_id = request.POST.get('username', '')
        reg = re.compile('^[a-zA-Z0-9]{4,12}$')

        if reg.match(user_id):

            try:
                user = UserModel.objects.get(username=user_id)
            except Exception as e:
                user = None

            result = {
                'result': 'success',
                'data': 'not exist' if user is None else 'exist'
            }
            return JsonResponse(result)

        else:

            result = {'result': 'fail'}
            return JsonResponse(result)


# 이메일 중복 확인 및 유효성 검사
@csrf_exempt
def email_check(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        reg = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        if reg.match(email):

            try:
                user = UserModel.objects.get(email=email)
            except Exception as e:
                user = None

            result = {
                'result': 'success',
                'data': 'not exist' if user is None else 'exist'
            }
            return JsonResponse(result)

        else:

            result = {'result': 'fail'}
            return JsonResponse(result)


def test(request):
    return render(request, 'my_page.html')
