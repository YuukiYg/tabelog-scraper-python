# coding: utf-8
import sys
import time
import requests
from bs4 import BeautifulSoup
import restaurant 

class TabelogScraper():
    def __init__(self):
        pass

    def __extract_text(self, element):
        if element is not None:
            return element.text.strip()
        else:
            return "-"

    def scrape(self, url):
        rest = restaurant.Restaurant()
        rest.url = url
        
        # htmlの抽出
        try:
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            bs = BeautifulSoup(response.text, 'html.parser')
        except:
            print("Error occured when extracting html from , from " + url)
            return rest # htmlが抽出できないとそれ以上解析ができないため、ここで終了する。
        
        # 店名の取得
        try:
            restaurant_name = self.__extract_text(bs.find(class_='display-name').find('span'))
            rest.name = restaurant_name
        except:
            print("Error occured when extracting restaurant name, from " + url)

        # ジャンルの取得（ジャンルは複数あるが、一番最初に出てきたジャンルを抽出することにする）
        try:
            # dtタグの値が 'ジャンル：' であるdlタグを探し、
            # そのdlタグ内で、実際のジャンル名が書かれているタグ(class名が'linktree__parent-target-text')を抽出する。
            target_dl_tags = bs.find(class_='rdheader-info-data').findAll('dl', {'class':'rdheader-subinfo__item'})
            for dl_tag in target_dl_tags:
                dt_tag = self.__extract_text(dl_tag.find('dt', {'class':'rdheader-subinfo__item-title'}))
                genre = ""
                if dt_tag == u'ジャンル：':
                    genre = self.__extract_text(dl_tag.find(class_='linktree__parent-target-text'))
                    break
            rest.genre = genre
        except:
            print("Error occured when extracting genre, from " + url)

        # 食べログスコアの取得
        try:
            score = self.__extract_text(bs.find(class_='rdheader-rating__score-val-dtl'))
            rest.score = score
        except:
            print("Error occured when extracting score, from " + url)

        # 夜の予算
        try:
            dinner_budget = self.__extract_text(bs.find(class_='gly-b-dinner'))
            rest.dinner_budget = dinner_budget
        except:
            print("Error occured when extracting dinner budget, from " + url)
    
        # 昼の予算
        try:
            lunch_budget = self.__extract_text(bs.find(class_='gly-b-lunch'))
            rest.lunch_budget = lunch_budget
        except:
            print("Error occured when extracting lunch budget, from " + url)

        # 所在地
        try:
            address = self.__extract_text(bs.find(class_='rstinfo-table__address'))
            rest.address = address
        except:
            print("Error occured when extracting address, from " + url)

        return rest


# Main処理
args = sys.argv
if len(args) == 2:
    path = args[1]
else:
    print("引数で入力ファイルを指定してください。")
    quit()

with open(path) as file:
    urls = file.readlines()

restaurant_list = []

# スクレイピングの呼び出し
for url in urls:
    url = url.rstrip() #末尾の改行を取る
    extracted_restaurant_info = TabelogScraper().scrape(url)
    restaurant_list.append(extracted_restaurant_info)
    
    print("解析完了:"+url)
    time.sleep(1)

# 結果の表示
print("名称" + "\t" + "ジャンル" + "\t" + "スコア" + "\t" + "夜の予算" + "\t" + "昼の予算" + "\t" + "所在地" + "\t" + "URL")
for r in restaurant_list:
        print(r.name + "\t" + r.genre + "\t" + r.score + "\t" + r.dinner_budget + "\t" + r.lunch_budget + "\t" + r.address + "\t" + r.url)