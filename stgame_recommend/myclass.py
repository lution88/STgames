# 크롤링 ImgPrice('URL') >> class.img()>> 'http~~~~~'
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup



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
#
# df = pd.read_csv('C:/Users/lutio/Desktop/13_stgames/stgames/steam_games.csv', encoding='utf-8')
# urls = df['url']
# game_list = []
# error_list = []
# for i, url in enumerate(urls):
#     u = url.split('/')[4]
#     if u == '':
#         error_list.append({i:u})
#         df.drop(index=i+1)
#         print(i)
#         continue
#     else:
#         game_list.append(u)
#
# print(error_list)
#     print(i, game_list[35165:35170])

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://store.steampowered.com/specials/',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
games = soup.select('#NewReleasesRows > a')
for game in games:
    image = game.select_one('div.tab_item_cap > img')['src']
    title = game.select_one('div.tab_item_content > div.tab_item_name').text
    discount_per = game.select_one('div.discount_block.tab_item_discount > div.discount_pct').text
    original_price = game.select_one('div.discount_block.tab_item_discount > div.discount_prices > div.discount_original_price').text
    discount_price = game.select_one('div.discount_block.tab_item_discount > div.discount_prices > div.discount_final_price').text
    print(image, title, discount_per, original_price, discount_price)

#title = NewReleasesRows > a:nth-child(1) > div.tab_item_content > div.tab_item_name
#title = NewReleasesRows > a:nth-child(2) > div.tab_item_content > div.tab_item_name

# 정가 = #NewReleasesRows > a:nth-child(1) > div.discount_block.tab_item_discount > div.discount_prices > div.discount_original_price
# 정가 = #NewReleasesRows > a:nth-child(2) > div.discount_block.tab_item_discount > div.discount_prices > div.discount_original_price
# 할인가 = #NewReleasesRows > a:nth-child(1) > div.discount_block.tab_item_discount > div.discount_prices > div.discount_final_price
# 할인가 = #NewReleasesRows > a:nth-child(2) > div.discount_block.tab_item_discount > div.discount_prices > div.discount_final_price
# 할인률 = #NewReleasesRows > a:nth-child(1) > div.discount_block.tab_item_discount > div.discount_pct
# 할인율 = #NewReleasesRows > a:nth-child(2) > div.discount_block.tab_item_discount > div.discount_pct
# img = div.tab_item_cap > img