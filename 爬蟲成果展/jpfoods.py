# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:17:48 2023

@author: willy
"""
'''
Chome console執行
檢查此元素是否可以被滑動

var element = document.querySelector('div.jsx-987803290.scroll-box');

undefined

var canScroll = element.scrollHeight > element.clientHeight;

undefined

canScroll

true


'''
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import db
import re

'''________________________________s  t  a  r  t________________________________'''  

driver = webdriver.Chrome()                                                    # 建立瀏覽器物件

driver.get('https://tabelog.com/tw/rstLst/')                                   # 使用driver 抓取網址

areas = ['東京','京都','北海道','大阪','沖繩']

for area in areas:
    
    driver.find_element(By.ID,"js-autocomplete-global-location").send_keys(area)# 找出可輸入元素並輸入字串
    
    driver.find_element(By.CSS_SELECTOR , 'input.c-btn.c-btn--primary.global-headline__search-btn').click()# 找出可點擊元素並點擊
    
    time.sleep(4)                                                              # 強制等待4秒確保抓取完整資料
    
    driver.find_element(By.ID , 'js-map-search-sort-trigger').click()          # 找出可點擊元素並點擊
    
    time.sleep(4)                                                              # 強制等待4秒確保抓取完整資料
    
    driver.find_element(By.CSS_SELECTOR , "span.js-map-search-sort-target[data-value='rt']").click()# 找出可點擊元素並點擊
    
    time.sleep(4)                                                              # 強制等待4秒確保抓取完整資料
    
    for i in range(2):
        data = driver.page_source                                              # 使用.page_soucre解析
        
        soup = BeautifulSoup(data , 'html.parser')                             # 帶入BeautifulSoup 用 html.parser解析 
        
        ul = soup.select_one('ul#js-map-search-result-list')
        
        titles = ul.select('p.list-rst__name small.list-rst__name-ja')
        links  = ul.select('p.list-rst__name a')
        imgs   = ul.select('p.list-rst__img img')
        groups = ul.select('ul.list-rst__area-catg')
        stars  = ul.select('b.c-rating__val')
            
        for title,link,img,group,star in zip(titles,links,imgs,groups,stars):
            print("標題: "+title.text)
            gr1 = group.select_one('li.list-rst__area').text.strip()
            gr2 = group.select_one('li.list-rst__catg').text.strip()
            print("分類: "+gr1+"-"+gr2)
            print("評價: "+star.text)
            print("連結: "+link.get('href'))
            if "https://tblg.k-img.com/restaurant/images/Rvw/" not in img.get('src'):
                print("圖片: "+'https://tblg.k-img.com/restaurant/images/Rvw/'+img.get('src'))
            else:
                print("圖片: "+img.get('src'))
            print()
            print()
            '''________________________________e  n  d________________________________'''  
    
            '''_______________________與sql連接_______________________'''
            
            # T = title.text
            # T = re.sub(r'[^\w\s]', '', T)  # 移除特殊符號
            # S = star.text
            # L = link.get('href')

            # if "https://tblg.k-img.com/restaurant/images/Rvw/" not in img.get('src'):
            #     P = 'https://tblg.k-img.com/restaurant/images/Rvw/'+img.get('src')
            # else:
            #     P = img.get('src')
                
    
            # sql = "select * from jpfoods where title = '{}' and platform = '{}'".format(T,area)
            
            # db.cursor.execute(sql)       #套用db.cursor的連線 執行變數sql70行
            
            # if db.cursor.rowcount == 0 : #抓整個比數如果等於0才可以新增
            #     sql = "insert into jpfoods(title,link_url,photo_url,star,platform) value('{}','{}','{}','{}','{}')".format(T,L,P,S,area)
            
            # db.cursor.execute(sql)       #使用db裡面的cursor方法執行sql語法
                    
            # db.conn.commit()             #使用db裡面的cursor方法必須調用此方法才能讓這些改變永久保存到資料庫
            
        driver.find_element(By.CSS_SELECTOR , 'a.c-pagination__target.c-pagination__target--next.js-pjax-anchor').click()
        
        time.sleep(5)
    
# db.conn.close()                      #關閉資料庫連接避免資源泄漏

driver.quit()
    
