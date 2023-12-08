# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 19:24:07 2023

@author: willy
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import os

def pinterest(seach):

    driver = webdriver.Chrome()                                                   
    
    driver.implicitly_wait(10)                                                   
        
    driver.get("https://www.pinterest.jp/ideas/")                                 
    
    driver.find_element(By.CSS_SELECTOR , "div.ujU.zI7.iyn.Hsu input").send_keys(seach + Keys.ENTER) 
    time.sleep(5)
    
    area = []
    
    for i in range(1):
    
        data = driver.page_source
        
        soup = BeautifulSoup(data , 'html.parser')                                     
        
        # with open('test.txt', 'w', encoding='utf8') as file:
        #     file.write(str(soup))
            
        photo = soup.select('div.XiG.zI7.iyn.Hsu img')
        
        for row in photo:
            # print(row.get('src'))
            
            if row not in area:
                area.append(row.get('src'))
            
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)') 
        time.sleep(5)
    
    driver.quit() 
    
    x = 1
    
    for line in area:
        
        if not os.path.exists(seach):
            os.makedirs(seach)
        
        try:
            w = requests.get(line)
        except requests.exceptions.RequestException as e:
            print(f"無法下載圖片 {line}: {e}")
            continue
        
        file = str(x) + '.jpg'
        
        with open (seach + '/' + file , 'wb') as fObj:
            fObj.write(w.content)
            
            x += 1
            time.sleep(1)
            
        print(line)


seach = input("請輸入搜尋內容 : ")

pinterest(seach)











