# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 11:12:50 2023

@author: willy
"""

from bs4 import BeautifulSoup
import requests
import urllib.parse
import threading
import csv
import os

def Cola(seach):
    
    session = requests.session()                                               
    url1    = 'https://www.colatour.com.tw/'                                  
    header  = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
              }                                                                
    data    = session.get(url1 , headers = header)                             
    p1 = 'DepartureCity=*'                                                    
    p2 = 'KeyWord={}'.format(seach)
    p3 = 'Source=00'
    url2    = 'https://www.colatour.com.tw/C10A_TourSell/C10A08_PatternSearch.aspx?{}&{}&{}'.format(p1,p2,p3)
    payload = {                                                               
                'DepartureCity': '*',
                'KeyWord': seach,
                'Source': '00'
                  }
    
    data    = session.get(url2 , headers = header , params = payload)          
    soup    = BeautifulSoup(data.text , 'html.parser')                         
    total   = soup.select('ul.tourin-city-list-block li')
    
    os.makedirs('Cola-icook', exist_ok=True)

    with open('Cola-icook/Cola.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)

        # 寫入一列資料
        writer.writerow(['標題', '連結', '圖片', '價格', '日期'])

        for row in total:
            title = row.select_one('div.tourin-city-list-name p')
            links = row.select_one('div.tourin-city-list-nameblock a')
            photos= row.select_one('div.pattern-imgpush a img')
            price = row.select_one('div.tourin-city-list-price p')
            date  = row.select_one('ul.tourin-city-list-date li')

            if title != None:
                link  = links.get('href')
                photo = photos.get('src') 
                # 寫入一列資料
                writer.writerow([title.text, 'https://www.colatour.com.tw'+link, photo, price.text, date.text])
            
    print("__________________________________")
    print('旅遊結束')
            
def delicious(seach1 , seach2):
    session = requests.session()                                             
    url1    = 'https://icook.tw/'
    header  = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
              }                                                                   
    data    = session.get(url1 , headers = header)                            
    soup    = BeautifulSoup(data.text , 'html.parser')                           
    url2    = 'https://icook.tw/recipes/search'                               
    payload = {'q': seach1,                                                    
                'ingredients': seach2,
                'page': ''
                }
    
    
    os.makedirs('Cola-icook', exist_ok=True)
    # 開啟CSV檔案並寫入資料
    with open('Cola-icook/icook.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)

        # 寫入一列資料
        writer.writerow(['標題', '連結', '圖片', '食材'])

        for i in range(2,3):
            data    = session.get(url2 , headers = header , data = payload)       
            soup    = BeautifulSoup(data.text , "html.parser")                      
            goods   = soup.select('li.browse-recipe-item')
            
            for row in goods:
                title = row.select_one('h2.browse-recipe-name').get('data-title')
                links = row.select_one('a.browse-recipe-link').get('href')
                foods = row.select_one('p',class_='browse-recipe-content-ingredient')
                photo = row.select_one('img',class_='browse-recipe-cover-img').get('data-src')
            
                # 寫入一列資料
                writer.writerow([title, 'https://icook.tw' + links, urllib.parse.unquote(photo), foods.text.strip()])
            
            payload['page'] = i
        
    print("__________________________________")
    print('愛料理結束')
        
t1 = threading.Thread(target = Cola , args = ('東京',))
t2 = threading.Thread(target = delicious , args = ('燒肉' , ''))
t1.start()
t2.start()
t1.join()
t2.join()

print('Done.')   