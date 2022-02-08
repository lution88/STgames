from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import EmailMessage

import re

from django.conf import settings
from django.contrib import messages

import requests
from bs4 import BeautifulSoup

from stgame_recommend.makeit_to_class import CollaborateFiltering

import numpy as np
import pandas as pd
import time
import tensorflow.compat.v1 as tf
import random
from collections import Counter
from sklearn.metrics import roc_curve, auc, average_precision_score
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stgames.settings')
django.setup()

from stgame_recommend.myclass import ImgPrice
from .models import RecommendGames, SimilarUser, Games, UserModel, FavoriteGames
# import random


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
    # 스팀 할인게임 크롤링
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://store.steampowered.com/specials/', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    games = soup.select('#NewReleasesRows > a')

    # 크롤링한 게임 리스트
    game_list = []
    i = 1
    for game in games:
        url = game['href']
        image = game.select_one('div.tab_item_cap > img')['src']
        title = game.select_one('div.tab_item_content > div.tab_item_name').text
        discount_per = game.select_one('div.discount_block.tab_item_discount > div.discount_pct').text
        original_price = game.select_one('div.discount_block.tab_item_discount > div.discount_prices > div.discount_original_price').text
        discount_price = game.select_one('div.discount_block.tab_item_discount > div.discount_prices > div.discount_final_price').text

        games_list = {
            'index': i,
            'url': url,
            'image': image,
            'title': title,
            'discount_per': discount_per,
            'original_price': original_price,
            'discount_price': discount_price
        }
        game_list.append(games_list)
        i += 1

    # 유저 별 게임 추천 리스트

    # 로그인한 유저의 id 확인
    user_id = request.user.id
    # 추천게임db에서 로그인한 사용자의 id를 확인하여 추천한 게임들을 가져온다.
    try:
        rec_games = RecommendGames.objects.get(user_id=user_id)
        rec = rec_games.rec_game.replace("'", '').replace("[", '').replace("]", '').split(', ') # 스트링자료를 리스트로 변환
    except:
        RecommendGames.objects.get(user_id=1)
        rec = rec_games.rec_game.replace("'", '').replace("[", '').replace("]", '').split(', ') # 스트링자료를 리스트로 변환
    # 랜덤한 이미지 가져오기.
    # a = Games.objects.filter(game__icontains='a')
    # ImgPrice(a[random.randrange(1, 10)].game_url).img()

    sim_user_game = SimilarUser.objects.all()
    for sim in sim_user_game:
        print(sim.sim_user)
        print(sim.sim_game_list)



    return render(request, 'main.html', {'games':game_list[:20], 'rec':rec[:10]})
    # return render(request, 'main.html', {'games':game_list[:20], 'rec_games':rec_games})


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
    return redirect('/sign-in/')


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


def find_id(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email', '')
        reg = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        if reg.match(email):

            # try:
            user = UserModel.objects.get(email=email)

            if user is not None:
                email_template = render_to_string('find_id_email_template.html',
                                                  {'username': user.username, 'nickname': user.nickname})
                method_email = EmailMessage(
                    '당신의 아이디가 메일에 있습니다.',
                    email_template,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                method_email.send(fail_silently=False)
                return render(request, 'sign_in_and_up.html', context)
            # except Exception as e:
            #     messages.info(request, '입력하신 아이디에 맞는 이메일이 없습니다. 다시 확인해 주세요!')
    context = {}
    return render(request, 'sign_in_and_up.html', context)


def find_pw(request):
    dd = ''
    return


def test(request):
    return render(request, 'my_page.html')

def take_url(request):
    df = pd.read_csv('C:/Users/lutio/Desktop/13_stgames/stgames/steam_games.csv', encoding='utf-8')
    urls = df['url']
    game_list = []
    for url in urls:
        try:
            u = url.split('/')[4]
            game_list.append(FavoriteGames(game_id=u))
        except:
            print('None')

    i = 0
    j = 1
    while True:
        try:
            FavoriteGames.objects.bulk_create(game_list[i:j])
            i = j
            j += 1
            print(f'{i}개 완료', )
            time.sleep(1)
        except:
            print("에러발생")
            i += 1
            j += 1
    return render(request, 'main.html')



def tensorflow(request):

    new_user = np.random.rand(1, 5064)
    apply_lambda = lambda x: 1 if x > 0.99 else 0
    new_user = new_user.reshape(5064, )
    tt = np.array([apply_lambda(xi) for xi in new_user])
    tt = tt.reshape(1, 5064)
    make_random_time = lambda x: random.randint(10, 90) if x == 1 else 0
    tt_time = np.array([make_random_time(xi) for xi in tt.reshape(5064, )])
    tt_time.reshape(5064, )

    temp = CollaborateFiltering(k=30)
    temp.add_new_user(tt_time)
    temp.train_data()

    recommend_result = temp.eval_result()
    print("추천게임 : ", recommend_result)

    similar_user = temp.recommend_sim_user()
    print("비슷한유저 : ", similar_user)

    user_id = request.user.id

    try:
        RecommendGames.objects.get(user_id=user_id)
        RecommendGames.objects.filter(user_id=user_id).update(rec_game=recommend_result)
        # a.update(rec_game=recommend_result)
        print("업데이트 완료")
    except:
        RecommendGames.objects.create(rec_game=recommend_result, user_id=user_id)
        print("작성완료")

    sim_user = []
    sim_user_game = []

    for user in similar_user:
        sim_user.append(user[0])
        sim_user_game.append(user[1])

    try:
        SimilarUser.objects.get(user_id=user_id)
        SimilarUser.objects.filter(user_id=user_id).update(sim_user=sim_user, sim_game_list=sim_user_game, user_id=user_id)
        print("sim 업데이트 완료")
    except:
        SimilarUser.objects.create(sim_user=sim_user, sim_game_list=sim_user_game, user_id=user_id)
        print("sim 작성완료")


    # all_info = RecommendGames.objects.all()
    # rec_info = all_info['rec_result']
    # sim_user = all_info['sim_user']
    # sim_game_list = all_info['sim_game_list']


    return render(request, 'main.html')


import random


# ajax 장고의 경우 request의 body에 객체를 담아서 보낸다
# 하지만 요청할때 method에 딕셔너리 형태로 가져와도 된다.
@csrf_exempt
def mypage(request):
    if request.method == 'GET':
        a = Games.objects.filter(game__icontains='a')
        print(a[1].game_url)
        print(ImgPrice(a[1].game_url).img())
        b = Games.objects.all().count()
        print(b)
        return render(request, 'my_page.html',
                      {'game': a[random.randrange(1, 100)], 'img': ImgPrice(a[random.randrange(1, 5)].game_url).img()})
    if request.method == 'POST':
        # word = request.body
        # lstrip 왼쪽 공백제거 앞쪽 공백 제거
        word = request.POST['search'].lstrip()
        if word == "":
            word = 9999999
        print(word)

        word = Games.objects.filter(game__icontains=word)

        good = list(word.values('game')[:10])
        print(good[:10])

        return JsonResponse({'game': good})


#     40832 40833
@csrf_exempt
def test2(request):
    if request.method == 'POST':
        game = request.POST['game_name']
        play_time = request.POST['play_time']
        print(game)
        print(play_time)
        print(request.user)
        user_id = request.user.id
        game_id = Games.objects.get(game=game).game_id
        print('user_id : ', user_id)
        print('game_id : ', game_id)

        dup_count = FavoriteGames.objects.filter(game_id=game_id) & FavoriteGames.objects.filter(
            user_id=user_id) & FavoriteGames.objects.filter(playtime=play_time)
        dup_count = dup_count.count()
        print(dup_count)

        if dup_count <= 0:
            FavoriteGames.objects.create(game_id=game_id, user_id=user_id, playtime=play_time)

        return JsonResponse({'msg': '무야호'})
    else:
        # new_user = np.random.rand(5064)
        # apply_lambda = lambda x: 1 if x > 0.99 else 0
        # print('aaaa',new_user)
        # # new_user = new_user.reshape(5064)
        # print(new_user)
        # tt = np.array([apply_lambda(xi) for xi in new_user])
        # print(tt.shape)
        # tt = tt.reshape(1, 5064)
        # make_random_time = lambda x: random.randint(10, 90) if x == 1 else 0
        # tt_time = np.array([make_random_time(xi) for xi in tt.reshape(5064, )])
        # tt_time.reshape(5064, )
        # print(tt_time)
        try:

            RecommendGames.objects.get(user_id=request.user.id)
        except :
            return render(request,'my_page.html')

        play_time_list = np.zeros(5064)
        print(play_time_list)

        fagame = FavoriteGames.objects.filter(user_id=request.user.id)
        beanList_1 = []
        beanList_2 = []
        for i in fagame:
            print(i.game_id)
            beanList_1.append(i.game_id)
            beanList_2.append(i.playtime)

        x = Games.objects.filter(game_id__in=beanList_1)
        a = CollaborateFiltering(k=30)
        beanList_1.clear()
        for i in range(len(x)):
            gamename = x.values('game')[i]['game']
            c = a.game2idx_origin[gamename]
            beanList_1.append(gamename)
            print(c)
            play_time_list[c] = beanList_2[i]
            print(beanList_2[i])

        print(play_time_list)

        a.add_new_user(play_time_list)
        a.train_data()
        print('user_game_name: ', beanList_1)
        print('test:', a.eval_result())
        print(a.recommend_sim_user())

        RecommendGames.objects.create(user_id=request.user.id , rec_game=a.eval_result())



        return render(request, 'my_page.html')
# test