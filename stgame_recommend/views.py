from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from .models import UserModel
from django.contrib import messages


def index(request):
    return render(request, 'sign_in_and_up.html')


def sign_in(request):
    if request.method == 'POST':
        user_id = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=user_id, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/main')
        else:
            messages.error(request, '아이디 혹은 비밀번호를 제대로 입력하세요!')
            return render(request, 'sign_in_and_up.html')

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/main')
        else:
            return render(request, 'sign_in_and_up.html')


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
            return render(request, 'sign_in_and_up.html', {'error': '비밀번호 잘 좀 적어봐요!'})
        else:
            if user_id == '' or password == '' or nickname == '' or email == '':
                return render(request, 'sign_in_and_up.html', {'error': '칸은 제발 채워주세요!!!'})

            exist_user = UserModel.objects.filter(username=user_id) or UserModel.objects.filter(email=email)
            if exist_user:
                return render(request, 'sign_in_and_up.html', {'error': '이미 있는 사람...중복확인 하고 가입하소!'})
            else:
                UserModel.objects.create_user(username=user_id, password=password, nickname=nickname, email=email)
                return render(request, 'sign_in_and_up.html')


@csrf_exempt
@login_required
def main(request):
    return render(request, 'main.html')


@csrf_exempt
@login_required
def my_page(request):
    return render(request, 'my_page.html')


@csrf_exempt
@login_required  # 사용자가 로그인 꼭 되어있어야 접근 가능함 표시
def logout(request):
    auth.logout(request)
    return redirect('')


@csrf_exempt
def id_check(request):
    if request.method == 'POST':
        user_id = request.POST.get('username', '')
        try:
            user = UserModel.objects.get(username=user_id)
        except Exception as e:
            user = None

        result = {
            'result': 'success',
            'data': 'not exist' if user is None else 'exist'
        }

        return JsonResponse(result)


@csrf_exempt
def email_check(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        try:
            user = UserModel.objects.get(email=email)
        except Exception as e:
            user = None

        result = {
            'result': 'success',
            'data': 'not exist' if user is None else 'exist'
        }

        return JsonResponse(result)
