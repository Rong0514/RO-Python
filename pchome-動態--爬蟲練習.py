# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:18:45 2023

@author: willy
"""

from selenium import webdriver

from bs4 import BeautifulSoup

import time

driver = webdriver.Chrome()                                                    # 建立瀏覽器物件

driver.implicitly_wait(10)                                                     # 隱性等待，最長等10秒

product = input("輸入想搜尋商品名稱:")
driver.get("https://ecshweb.pchome.com.tw/search/v3.3/?q="+product)            # 使用driver 抓取網址

data = driver.page_source                                                      # 使用.page_soucre解析

for i in range(100):
    
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')     # 滑動到底部載入所有資料
    
    time.sleep(3)                                                              # 強制等待3秒確保抓取完整資料                 
    
    soup = BeautifulSoup(data,'html.parser')                                   # 帶入BeautifulSoup 用 html.parser解析 
    
    titles = soup.select('h5.prod_name a')
    prices = soup.select('span.value')
    
    for title,price in zip(titles,prices):
        print("標題: ", title.text)
        print('價格: $'+ price.text+'NT')
        print()
