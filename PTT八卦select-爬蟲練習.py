# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 16:35:34 2023

@author: willy
"""

import requests

from bs4 import BeautifulSoup

from datetime import datetime

def PPT(search):

    header = {
        'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                }                                        # 瀏覽器代理用戶(標頭)
        
    '''________________________________傳送第一次請求__解鎖over18的要求________________________________'''  
    
    payload = {'from': '/bbs/Gossiping/index.html',
               'yes': 'yes'
               }                                         # payload 要求
    
    session = requests.session()                         # 以session方式做請求
    
    url1    = 'https://www.ptt.cc/ask/over18'            # 請求的網址
    
    session.post(url1,headers = header , data = payload) # 將網址、要求、代理用戶以session.post方式送回去
    
    '''________________________________傳送第二次請求__抓取當前網頁資訊________________________________'''
        
    url2    = 'https://www.ptt.cc/bbs/Gossiping/index.html' # 請求的網址
    
    while True:
        
        area   = session.post(url2,headers=header,data=payload) # 將網址、要求、代理用戶以session.post方式送回去
        
        temp   = area.text.split('<div class="r-list-sep"></div>')[0] 
                            # 定義temp將area.text以'<div class="r-list-sep"></div>'設定為切割符號並抓取索引值0
        
        soup1  = BeautifulSoup(temp,'html.parser')          # area帶入BeautifulSoup解析(用html.parser方式)
        
        titles = soup1.select('div.r-ent div.title a')      #以select抓取標籤.class 下層 標籤.class 下層 元素
        times  = soup1.select('div.r-ent div.meta div.date')#以select抓取標籤.class 下層 標籤.class 下層 標籤.class
        
        Date   = datetime.now()                             # 設變數 > 抓取今天時間
        today  = str(Date.month)+"/"+str(Date.day)          # 設變數 > 將今天時間以字串方式篩選 成 月/日
        
        url2   = "https://www.ptt.cc"+soup1.select('div.btn-group.btn-group-paging a')[1].get("href")
                            # 將 url2請求網址 重新定義成 上一頁的網址 > 以無窮迴圈進行無限上一頁
    
        for title,time in zip(titles,times):
            if today != time.text:                          # 如果 今天時間 != 抓取時間時 傳送空值 = 變相離開迴圈
                return
            if "Re:" not in title.text and search in title.text:
                # 如果 "Re:" 不再 title.text裡面 且 search在裡面 則輸出
                print(title.text)
                
                '''________________________傳送第三次請求__抓取網頁資訊的下層內容________________________'''
                
                url3    = "https://www.ptt.cc" + title.get("href")             # 請求的網址
                
                item    = session.get(url3,headers = header)
                    
                soup2   = BeautifulSoup(item.text,'html.parser')               # 進行解析
                
                content = soup2.select_one("div#main-content")                 # 抓取內容
                
                upsplit = soup2.select("div#main-content div.article-metaline")[2].text
                
                dowsplit= '※ 發信站: 批踢踢實業坊(ptt.cc)'

                print(content.text.split(upsplit)[1].split(dowsplit)[0])
                            #輸出content內容以upsplit切割並抓取索引值1 二次切割dowsplit並抓取索引值0
                print(time.text)
                print("_"*45)


search = input("輸入搜尋: ")
PPT(search)
