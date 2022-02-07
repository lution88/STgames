import random

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, resolve_url

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import EmailMessage

import re

from django.conf import settings
from .models import UserModel
from django.contrib import messages

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, \
                                      PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import reverse_lazy


# 시작 페이지(로그인 및 회원가입)
def index(request):
    return render(request, 'sign_in_and_up.html')


# 로그인
@csrf_exempt
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
@csrf_exempt
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


# 아이디 찾기 함수
@csrf_exempt
def find_id(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email', '')
        reg = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        if reg.match(email):

            try:
                user = UserModel.objects.get(email=email)

                if user is not None:
                    email_template = render_to_string('find_id_email_template.html',
                                                      {'username': user.username, 'nickname': user.nickname})
                    method_email = EmailMessage(
                        '회원님의 아이디가 도착했습니다.',
                        email_template,
                        settings.EMAIL_HOST_USER,
                        [email]
                    )
                    method_email.send(fail_silently=False)
                    return render(request, 'sign_in_and_up.html', context)
            except Exception as e:
                messages.info(request, '입력한 이메일이 없습니다. 다시 확인해 주세요!')
    context = {}
    return render(request, 'sign_in_and_up.html', context)


# 비밀번호 찾기 함수
@csrf_exempt
def find_pw(request):
    if request.method == 'POST':
        user_id = request.POST.get('username', '')

        try:
            user = UserModel.objects.get(username=user_id)

            if user is not None:
                return redirect('/password_reset')
        except Exception as e:
            messages.info(request, '입력한 아이디가 없습니다. 다시 확인해 주세요!')
    return render(request, 'sign_in_and_up.html')


# 비밀번호 초기화 메일 보내기
class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm

    def form_valid(self, form):
        if UserModel.objects.filter(email=self.request.POST.get('email')).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'password_reset_done_fail.html')


# 비밀번호 초기화 메일 보내기 성공
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


# 새 비밀번호 설정
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = SetPasswordForm

    def form_valid(self, form):
        return super().form_valid(form)


# 새 비밀번호 설정 완료
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url('sign_in_and_up.html')
        return context


def test(request):
    return render(request, 'my_page.html')
