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
                }                                       
    
    payload = {'from': '/bbs/Gossiping/index.html',
               'yes': 'yes'
               }                                         
    
    session = requests.session()                         
    
    url1    = 'https://www.ptt.cc/ask/over18'            
    
    session.post(url1,headers = header , data = payload) 
    
    
        
    url2    = 'https://www.ptt.cc/bbs/Gossiping/index.html' 
    
    while True:
        
        area   = session.post(url2,headers=header,data=payload) 
        
        temp   = area.text.split('<div class="r-list-sep"></div>')[0] 
                           
        
        soup1  = BeautifulSoup(temp,'html.parser')        
        
        titles = soup1.select('div.r-ent div.title a')      
        times  = soup1.select('div.r-ent div.meta div.date')
        
        Date   = datetime.now()                           
        today  = str(Date.month)+"/"+str(Date.day)          
        
        url2   = "https://www.ptt.cc"+soup1.select('div.btn-group.btn-group-paging a')[1].get("href")
                           
    
        for title,time in zip(titles,times):
            if today != time.text:                        
                return
            if "Re:" not in title.text and search in title.text:
              
                print(title.text)
                
                
                
                url3    = "https://www.ptt.cc" + title.get("href")             
                
                item    = session.get(url3,headers = header)
                    
                soup2   = BeautifulSoup(item.text,'html.parser')               
                
                content = soup2.select_one("div#main-content")               
                
                upsplit = soup2.select("div#main-content div.article-metaline")[2].text
                
                dowsplit= '※ 發信站: 批踢踢實業坊(ptt.cc)'

                print(content.text.split(upsplit)[1].split(dowsplit)[0])
                         
                print(time.text)
                print("_"*45)


search = input("輸入搜尋: ")
PPT(search)
