# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 10:20:44 2023

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
        links = soup.select('div[data-test-id=deeplink-wrapper] a')
        for row in links:
            href = 'https://www.pinterest.jp' + row.get('href')
            if href not in area:
                area.append(href)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)') 
        time.sleep(5)
    driver.quit() 
    return area

def photo(area , seach):
    driver = webdriver.Chrome()                                                   
    data = []
    driver.implicitly_wait(10)                                                   
    for i in area:
        driver.get(i) 
        time.sleep(4)
        photos = driver.find_element(By.CSS_SELECTOR , 'div[data-test-id=pin-closeup-image] img')
        photo = photos.get_attribute('src')
        data.append(photo)
    driver.quit()

    x = 1
    for line in data:
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
area = pinterest(seach)
photo(area, seach)