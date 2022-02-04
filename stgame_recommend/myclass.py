# 크롤링 ImgPrice('URL') >> class.img()>> 'http~~~~~'
from re import U
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np




class ImgPrice:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    def img(self):
        result = self.soup.select_one('#gameHeaderImageCtn > img')
        result = result['src']
        return result

    def price(self):
        result = self.soup.select_one('#dlc_purchase_action > .game_purchase_price').getText().split()[1]
        return result

    def title(self):
        result = self.soup.select_one('#appHubAppName').getText()
        return result

# print(ImgPrice('https://store.steampowered.com/app/1043870/Dark_Forest/').price())

# 클래스#appHubAppName


def take_url(file):
    df = pd.read_csv(f'/home/tete/stgames/{file}', encoding='utf-8')
    urls = df['url']
    game_list = []
    for url in urls:
        try:
            u = url.split('/')[4]
            game_list.append(u)
        except:
            print('None')
    return game_list
game_id = take_url('steam_games.csv')[:100]
print(game_id)