# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import requests

from bs4 import BeautifulSoup

import json

import re

url    =  'https://tw.buy.yahoo.com/search/product'                            # 請求的網址

header = {
    'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }                                                                          # 瀏覽器代理用戶(標頭)
    
param  = {}                                                                    #HTTP要求的參數
p = input('請輸入查詢的商品：')
param['p'] = p                                                  

'''________________________________傳送第一次請求__抓取當前網頁資訊________________________________'''

data   = requests.get(url,params=param,headers=header).text                    # 將網址、請求參數、標頭以requests.get方式送回去

soup   = BeautifulSoup(data,'html.parser')

ul     = soup.find(id='isoredux-data')

item   = ul.string                                                             #在HTML元素只有一個子節點時返回文字，有多個子節點返回None

pattern = 'window.ISO_REDUX_DATA='                                             #正規表達式(要被取代內容)

uls    = re.sub(pattern,'', item)                                              #re.sub(被取代,取代,原字串) > 較彈性

uls    = uls.replace(";",'')                                                   #.replace(被取代,取代) > 較固定

goods  = json.loads(uls)                                                       # json.load = 讀取、json.loads = 解析

searchgoods = goods['search']['ecsearch']['hits']

for item in searchgoods:
    
    info = item['ec_description'].replace("\n",'').replace("\r",'').replace("　　　",'').replace(" ",'')

    if item['pres_data'].get('pictureurl') != None:
        
        
        if len(item['ec_promotional_item']) == 0:
            price = item['pres_data']['creditprice']
        else:
              price = item['ec_promotional_item'][0]['promo_price']
              
        photo = item['pres_data']['pictureurl']
        link  = item['pres_data']['producturl']
        title = item['pres_data']['productname_disp'].replace("\n",'').replace("\r",'').replace("  ",'').replace(" ",'')
        
        print("標題: "+title)
        print("連結: "+link)
        print("圖片: "+photo)
        print("價格:",price)
        print("說明: "+info)
        print()

