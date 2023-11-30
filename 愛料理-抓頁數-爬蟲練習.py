# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 00:36:33 2023

@author: willy
"""

from bs4 import BeautifulSoup

import requests

import urllib.parse

'''________________________________s  t  a  r  t____________________________'''  

def delicious(seach1 , seach2):

    session = requests.session()                                               # 以session方式做保持連接
    
    url1    = 'https://icook.tw/'                                              # 請求網址
    
    header  = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
              }                                                                # 瀏覽器代理用戶(標頭)
        
    '''________________________________傳送第一次請求__進入網頁_______________'''  
    
    data    = session.get(url1 , headers = header)                             # 將網址、標頭以session.get方式送回去
    
    soup    = BeautifulSoup(data.text , 'html.parser')                         # 帶入BeautifulSoup 用 html.parser解析 
    
    '''________________________________傳送第二次請求__進入搜尋頁面___________'''  
    
    url2    = 'https://icook.tw/recipes/search'                                # 請求網址
    
    payload = {'q': seach1,                                                    # payload要求  
                'ingredients': seach2,
                'page': ''
                }
    
    for i in range(2,100):
    
        data    = session.get(url2 , headers = header , data = payload)        # 將網址、payload要求、標頭以 requests.get方式送回去
        
        soup    = BeautifulSoup(data.text , "html.parser")                     # 帶入BeautifulSoup 用 html.parser解析 
        
        goods   = soup.select('li.browse-recipe-item')
        
        for row in goods:
            title = row.select_one('h2.browse-recipe-name').get('data-title')
            links = row.select_one('a.browse-recipe-link').get('href')
            foods = row.select_one('p',class_='browse-recipe-content-ingredient')
            photo = row.select_one('img',class_='browse-recipe-cover-img').get('data-src')
        
            print('標題:', title)
            print("連結: "+'https://icook.tw' + links)
            print("圖片: "+urllib.parse.unquote(photo))
            print(foods.text.strip())
            print()
            
            
        payload['page'] = i

'''________________________________e  n  d__________________________________'''  
    
seach1  = input("輸入食譜名: ")
seach2  = input("搜尋食材，以 , 分開: ")

delicious(seach1, seach2)


