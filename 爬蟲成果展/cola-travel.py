# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 01:03:19 2023

@author: willy
"""

from bs4 import BeautifulSoup
import requests
import db

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
        date  = row.select_one('ul.tourin-city-list-date li')

        if title != None:
            link  = links.get('href')
            photo = photos.get('src') 
            print("標題: "+title.text)
            print("連結: "+'https://www.colatour.com.tw'+link)
            print("圖片: "+photo)
            print("價格: "+price.text)
            print(date.text)
            print("_"*50)
            print()
        
        '''________________________________e  n  d__________________________'''  
        
        '''_______________________與sql連接_______________________'''
        # if title != None:
        #     link  = links.get('href')
        #     photo = photos.get('src') 
        #     T     = title.text
        #     L     = 'https://www.colatour.com.tw'+link
        #     P     = photo
        #     price = price.text
        #     Date  = date.text
            
        #     sql = "select * from travel where title = '{}' and platform = '台灣'".format(T)
            
        #     db.cursor.execute(sql)       #套用db.cursor的連線 執行變數sql70行
            
        #     if db.cursor.rowcount == 0 : #抓整個比數如果等於0才可以新增
        #         sql = "insert into travel(title,link_url,photo_url,price,date,platform) value('{}','{}','{}','{}','{}','台灣')".format(T,L,P,price,Date)
            
        #     db.cursor.execute(sql)       #使用db裡面的cursor方法執行sql語法
                    
        #     db.conn.commit()             #使用db裡面的cursor方法必須調用此方法才能讓這些改變永久保存到資料庫
        
    
    # db.conn.close()                      #關閉資料庫連接避免資源泄漏


seach = input("請輸入關鍵字: ")
Cola(seach)