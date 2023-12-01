# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 14:45:48 2023

@author: willy
"""

'''pip install selenium'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.parse
import time
import re
import db

driver = webdriver.Chrome()                                                    # 建立瀏覽器物件

driver.implicitly_wait(10)                                                     # 隱性等待，最長等10秒
    
driver.get("https://ifoodie.tw/explore/list?sortby=rating")                    # 使用driver 抓取網址

for i in range(10):                                                            #帶入迴圈抓頁數 

    element = driver.find_element(By.CSS_SELECTOR,'div.jsx-987803290.scroll-box') # 找出可以滑動元素
    
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element) # 滑動到底部載入所有資料
    
    time.sleep(5)                                                              # 強制等待5秒確保抓取完整資料
    
    data  = driver.page_source                                                 # 使用.page_soucre解析
    
    soup  = BeautifulSoup(data , 'html.parser')                                # 帶入BeautifulSoup 用 html.parser解析
    
    total = soup.select_one('div.jsx-987803290.item-list')
    title = total.select('div.jsx-1309326380.title a')
    addre = total.select('div.jsx-1309326380.address-row')
    photo = total.select('div.jsx-1309326380.restaurant-info img')
    
    for row1,row2,row3 in zip(title,photo,addre): 
        print("標題: "+row1.text)
        print("連結: "+'https://ifoodie.tw/'+urllib.parse.unquote(row1.get('href'))) # 使用 urllib.parse.unquote 解碼中文網址
        
        if row2.get('src') == 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==':
            print("圖片: "+row2.get('data-src'))
        else:
            print("圖片: "+row2.get('src'))
            
        print("地址:",row3.text)
        print()
        
        
        '''_______________________與sql連接_______________________'''
        
        # T   = row1.text
        # T = re.sub(r'[^\w\s]', '', T)  # 移除特殊符號
        # L   = 'https://ifoodie.tw/'+urllib.parse.unquote(row1.get('href'))
        # if row2.get('src') == 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==':
        #     IMG = row2.get('data-src')
        # else:
        #     IMG = row2.get('src')
    
        # add = row3.text
    
        # sql = "select * from ifoods where title = '{}' and platform = '愛食記'".format(T)
        
        # db.cursor.execute(sql)       #套用db.cursor的連線 執行變數sql70行
        
        # if db.cursor.rowcount == 0 : #抓整個比數如果等於0才可以新增
        #     sql = "insert into ifoods(title,link_url,photo_url,address,platform) value('{}','{}','{}','{}','愛食記')".format(T,L,IMG,add)
        
        # db.cursor.execute(sql)       #使用db裡面的cursor方法執行sql語法
                
        # db.conn.commit()             #使用db裡面的cursor方法必須調用此方法才能讓這些改變永久保存到資料庫

    driver.find_element(By.CSS_SELECTOR,"li.next a").click()                   # 找出可點擊下一頁元素
    time.sleep(5)                                                              # 強制等待5秒確保抓取完整資料

# db.conn.close()                      #關閉資料庫連接避免資源泄漏

driver.quit()                                                                  # 關閉瀏覽器