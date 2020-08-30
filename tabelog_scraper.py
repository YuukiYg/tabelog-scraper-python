# coding: utf-8
import sys
import time
import requests
from bs4 import BeautifulSoup

class TabelogScraper():
    def __init__(self):
        pass

    def __extract_text(self, element):
        if element is not None:
            return element.text.strip()
        else:
            return element

    def scrape(self, url):
        # htmlの抽出
        try:
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            bs = BeautifulSoup(response.text, 'html.parser')
        except:
            print("Error occured when extracting html from url: " + url)
            return "ERROR. URL=" + url
           
        # 店名の取得
        try:
            restaurant_name = self.__extract_text(bs.find(class_='display-name').find('span'))
        except:
            print("Error occured when extracting restaurant name")
            return "ERROR. URL=" + url

        # ジャンルの取得（ジャンルは複数あるが、一番最初に出てきたジャンルを抽出することにする）
        try:
            subinfo_items = bs.find(class_='rdheader-info-data').findAll('dl', {'class':'rdheader-subinfo__item'})
            for item in subinfo_items:
                dt_tag = self.__extract_text(item.find('dt', {'class':'rdheader-subinfo__item-title'}))
                genre = ""
                if dt_tag == u'ジャンル：':
                    genre = self.__extract_text(item.find(class_='linktree__parent-target-text'))
                    break
        except:
            print("Error occured when extracting genre")
            return "ERROR. URL=" + url


        # 食べログスコアの取得
        try:
            score = self.__extract_text(bs.find(class_='rdheader-rating__score-val-dtl'))
        except:
            print("Error occured when extracting score")
            return "ERROR. URL=" + url

        # 夜の予算
        try:
            dinner_budget = self.__extract_text(bs.find(class_='gly-b-dinner'))
        except:
            print("Error occured when extracting dinner budget")
            return "ERROR. URL=" + url
    
        # 昼の予算
        try:
            lunch_budget = self.__extract_text(bs.find(class_='gly-b-lunch'))
        except:
            print("Error occured when extracting lunch budget")
            return "ERROR. URL=" + url

        # 所在地
        try:
            address = self.__extract_text(bs.find(class_='rstinfo-table__address'))
        except:
            print("Error occured when extracting address")
            return "ERROR. URL=" + url

        # 結果の表示
        print(restaurant_name + "\t" + genre + "\t" + score + "\t" + dinner_budget + "\t" + lunch_budget + "\t" + address + "\t" + url)


# Main処理
args = sys.argv
if len(args) == 2:
    path = args[1]
else:
    print("引数で入力ファイルを指定してください。")
    quit()

with open(path) as file:
    urls = file.readlines()

# 結果の表示
print("名称" + "\t" + "ジャンル" + "\t" + "スコア" + "\t" + "夜の予算" + "\t" + "昼の予算" + "\t" + "所在地" + "\t" + "URL")
for url in urls:
    url = url.rstrip() #末尾の改行を取る
    TabelogScraper().scrape(url)
    time.sleep(1)
