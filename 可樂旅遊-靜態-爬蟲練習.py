# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 01:03:19 2023

@author: willy
"""

from bs4 import BeautifulSoup

import requests

'''________________________________s  t  a  r  t____________________________'''  

def Cola(seach):
    
    session = requests.session()                                               # 以session方式做保持連接
    
    url1    = 'https://www.colatour.com.tw/'                                   # 請求網址
    
    header  = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
              }                                                                # 瀏覽器代理用戶(標頭)
    
    '''________________________________傳送第一次請求__進入網頁_______________'''  
 
    data    = session.get(url1 , headers = header)                             # 將網址、標頭以session.get方式送回去
    
    p1 = 'DepartureCity=*'                                                     # 補足網址要求並給予彈性
    p2 = 'KeyWord={}'.format(seach)
    p3 = 'Source=00'
    
    url2    = 'https://www.colatour.com.tw/C10A_TourSell/C10A08_PatternSearch.aspx?{}&{}&{}'.format(p1,p2,p3)
                                                                               # 請求網址
                                                                                
    payload = {                                                                # payload要求  
                'DepartureCity': '*',
                'KeyWord': seach,
                'Source': '00'
                  }
    
    '''________________________________傳送第二次請求__進入搜尋頁面___________'''  
    
    data    = session.get(url2 , headers = header , params = payload)          # 將網址、payload要求、標頭以 requests.get方式送回去
    
    soup    = BeautifulSoup(data.text , 'html.parser')                         # 帶入BeautifulSoup 用 html.parser解析 
    
    total   = soup.select('ul.tourin-city-list-block li')
    
    for row in total:
        
        title = row.select_one('div.tourin-city-list-name p')
        links = row.select_one('div.tourin-city-list-nameblock a')
        photos= row.select_one('div.pattern-imgpush a img')
        price = row.select_one('div.tourin-city-list-price p')
        
        if title != None:
            link  = links.get('href')
            photo = photos.get('src') 
            print("標題: "+title.text)
            print("連結: "+'https://www.colatour.com.tw'+link)
            print("圖片: "+photo)
            print("價格: "+price.text)
            print("_"*50)
            print()
        
'''________________________________e  n  d__________________________________'''  

    
seach = input("請輸入關鍵字: ")
Cola(seach)
