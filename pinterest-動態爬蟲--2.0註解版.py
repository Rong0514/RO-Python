# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 10:37:07 2023

@author: willy
"""

from selenium import webdriver                                              # 引入webdriver模組
from selenium.webdriver.common.by import By                                 # 引入By類別
from selenium.webdriver.common.keys import Keys                             # 引入Keys類別
import time                                                                 # 引入time模組
from bs4 import BeautifulSoup                                               # 引入BeautifulSoup類別
import requests                                                             # 引入requests模組
import os                                                                   # 引入os模組
from selenium.common.exceptions import NoSuchElementException               # 引入NoSuchElementException類別

def LINK(seach):                                                            # 定義一個函數來搜索Pinterest
    driver = webdriver.Chrome()                                             # 創建一個Chrome瀏覽器實例
    driver.implicitly_wait(5)                                               # 設置隱式等待時間為5秒
    driver.get("https://www.pinterest.jp/ideas/")                           # 打開Pinterest的搜索頁面
    driver.find_element(By.CSS_SELECTOR , "div.ujU.zI7.iyn.Hsu input").send_keys(seach + Keys.ENTER)  # 在搜索框中輸入搜索詞並按Enter
    time.sleep(5)                                                           # 等待5秒以便頁面加載
    
    area = []                                                               # 創建一個空列表來存儲鏈接
    
    for i in range(5):                                                      # 循環5次
        data = driver.page_source                                           # 獲取頁面源碼
        soup = BeautifulSoup(data , 'html.parser')                          # 使用BeautifulSoup解析頁面源碼
        links = soup.select('div[data-test-id=deeplink-wrapper] a')         # 從頁面中選擇所有的鏈接
        
        for row in links:                                                   # 對於每一個鏈接
            href = 'https://www.pinterest.jp' + row.get('href')             # 獲取鏈接的href屬性並添加到基礎URL上
            if href not in area:                                            # 如果這個鏈接還沒有被添加到列表中
                area.append(href)                                           # 將這個鏈接添加到列表中
                
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 滾動到頁面的底部
        time.sleep(2)                                                      # 等待2秒以便頁面加載
        
    driver.quit()                                                           # 關閉瀏覽器實例
    print("總共 : ",len(area),'筆')                                         # 打印出鏈接的數量
    
    return area                                                             # 返回鏈接列表



def PHOTO(area, seach):                                                                 # 定義一個函數來下載Pinterest的圖片
    driver = webdriver.Chrome()                                                         # 創建一個Chrome瀏覽器實例
    data = []                                                                           # 創建一個空列表來存儲圖片URL
    driver.implicitly_wait(3)                                                           # 設置隱式等待時間為3秒
    for i in area:                                                                      # 對於每一個鏈接
        driver.get(i)                                                                   # 打開鏈接
        time.sleep(1)                                                                   # 等待1秒以便頁面加載
        body_text = driver.find_element(By.TAG_NAME, "body").text                       # 獲取頁面的文本內容
        if "內容創作者已移除這個內容" in body_text:                                       # 如果頁面中有這個文本
            continue                                                                    # 繼續下一次循環
        try:                                                                            # 嘗試
            video = driver.find_element(By.CSS_SELECTOR , 'div.iCM.XiG.L4E.o5r video')  # 獲取頁面中的視頻元素
            photo_url = video.get_attribute('poster')                                   # 獲取視頻的poster屬性（即視頻的封面圖片）
        except NoSuchElementException:                                                  # 如果找不到視頻元素
            try:                                                                        # 嘗試
                videos = driver.find_element(By.CSS_SELECTOR , 'div[data-test-id=story-pin-closeup] img')  # 獲取頁面中的圖片元素
                photo_url = videos.get_attribute('src')                                 # 獲取圖片的src屬性（即圖片的URL）
            except NoSuchElementException:                                              # 如果找不到圖片元素
                try:                                                                    # 嘗試
                    photo = driver.find_element(By.CSS_SELECTOR , 'div[data-test-id=pin-closeup-image] img')  # 獲取頁面中的圖片元素
                    photo_url = photo.get_attribute('src')                              # 獲取圖片的src屬性（即圖片的URL）
                except NoSuchElementException:                                          # 如果找不到圖片元素
                    continue                                                            # 繼續下一次循環
        data.append(photo_url)                                                          # 將圖片URL添加到列表中
        
        print("目前載入 : ",len(data),"/",len(area))                                     # 打印出當前已經加載的圖片數量和總數
        
    driver.quit()                                                                       # 關閉瀏覽器實例

    x = 1                                                                               # 設置一個變數來計數
    
    for line in data:                                                                   # 對於每一個圖片URL
        if not os.path.exists(seach):                                                   # 如果搜索詞的文件夾還不存在
            os.makedirs(seach)                                                          # 創建一個新的文件夾
            
        try:                                                                            # 嘗試
            w = requests.get(line)                                                      # 下載圖片
        except requests.exceptions.RequestException as e:                               # 如果出現異常（例如，URL無效，網絡連接問題等）
            print(f"無法下載圖片 {line}: {e}")                                           # 打印錯誤信息
            continue                                                                    # 繼續下一次循環
            
        if '.gif' in line:                                                              # 如果圖片URL中包含'.gif'
            file = str(x) + '.gif'                                                      # 創建一個新的文件名
        else:                                                                           # 否則
            file = str(x) + '.jpg'                                                      # 創建一個新的文件名
        
        with open (seach + '/' + file , 'wb') as fObj:                                  # 打開一個新的文件
            fObj.write(w.content)                                                       # 將圖片內容寫入文件
            x += 1                                                                      # 將計數變數加1
            time.sleep(1)                                                               # 等待1秒
        print(line)                                                                     # 打印圖片URL


seach = input("請輸入搜尋內容 : ")                                                        # 請求用戶輸入搜索詞
area  = LINK(seach)                                                                     # 調用LINK函數來搜索Pinterest並獲取鏈接列表
PHOTO(area, seach)                                                                      # 調用PHOTO函數來下載圖片 
