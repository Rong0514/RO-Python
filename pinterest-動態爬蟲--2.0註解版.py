# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 10:37:07 2023

@author: willy
"""

from selenium import webdriver                                               # 引入webdriver模組
from selenium.webdriver.common.by import By                                  # 引入By模組
from selenium.webdriver.common.keys import Keys                              # 引入Keys模組
from selenium.webdriver.support.ui import WebDriverWait                      # 引入WebDriverWait模組
from selenium.webdriver.support import expected_conditions as EC             # 引入expected_conditions模組並命名為EC
import time                                                                  # 引入time模組
from bs4 import BeautifulSoup                                                # 引入BeautifulSoup模組
import requests                                                              # 引入requests模組
import os                                                                    # 引入os模組
from selenium.common.exceptions import NoSuchElementException                # 引入NoSuchElementException模組

def LINK(seach):                                                             # 定義LINK函數
    driver = webdriver.Chrome()                                              # 創建Chrome瀏覽器驅動實例
    driver.implicitly_wait(3)                                                # 隱式等待3秒
    driver.get("https://www.pinterest.jp/ideas/")                            # 打開Pinterest網站
    driver.find_element(By.CSS_SELECTOR , "div.ujU.zI7.iyn.Hsu input").send_keys(seach + Keys.ENTER)  # 在搜索框中輸入搜索詞並按Enter
    wait = WebDriverWait(driver, 10)                                         # 創建WebDriverWait實例
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))        # 等待直到body元素出現

    area = []                                                                # 創建空列表area

    for i in range(5):                                                       # 迴圈5次
        data  = driver.page_source                                           # 獲取頁面源碼
        soup  = BeautifulSoup(data , 'html.parser')                          # 使用BeautifulSoup解析頁面源碼
        links = soup.select('div[data-test-id=deeplink-wrapper] a')          # 從解析結果中選擇特定元素

        for row in links:                                                    # 迴圈遍歷links
            href = 'https://www.pinterest.jp' + row.get('href')              # 獲取每個元素的href屬性並拼接URL
            if href not in area:                                             # 如果URL不在area列表中
                area.append(href)                                            # 將URL添加到area列表中

        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 滾動頁面到底部
        time.sleep(2)                                                        # 等待2秒

    driver.quit()                                                            # 關閉瀏覽器驅動實例
    print("總共 : ",len(area),'筆')                                           # 輸出area列表的長度

    return area                                                              # 返回area列表
                                                         



def PHOTO(area, seach):                                                                 # 定義PHOTO函數
    driver = webdriver.Chrome()                                                         # 創建Chrome瀏覽器驅動實例
    data   = []                                                                         # 創建空列表data
    driver.implicitly_wait(3)                                                           # 隱式等待3秒
    for i in area:                                                                      # 迴圈遍歷area列表
        driver.get(i)                                                                   # 打開URL
        wait = WebDriverWait(driver, 10)                                                # 創建WebDriverWait實例
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))               # 等待直到body元素出現
        body_text = driver.find_element(By.TAG_NAME, "body").text                       # 獲取body元素的文本
        if "內容創作者已移除這個內容" in body_text:                                        # 如果文本中包含特定字符串
            continue                                                                    # 繼續下一次迴圈
        try:                                                                            # 嘗試執行以下代碼
            video     = driver.find_element(By.CSS_SELECTOR , 'div.iCM.XiG.L4E.o5r video')  # 尋找特定元素
            photo_url = video.get_attribute('poster')                                   # 獲取元素的poster屬性
        except NoSuchElementException:                                                  # 如果找不到元素
            try:                                                                        # 嘗試執行以下代碼
                videos    = driver.find_element(By.CSS_SELECTOR , 'div[data-test-id=story-pin-closeup] img')  # 尋找特定元素
                photo_url = videos.get_attribute('src')                                 # 獲取元素的src屬性
            except NoSuchElementException:                                              # 如果找不到元素
                try:                                                                    # 嘗試執行以下代碼
                    photo     = driver.find_element(By.CSS_SELECTOR , 'div[data-test-id=pin-closeup-image] img')  # 尋找特定元素
                    photo_url = photo.get_attribute('src')                              # 獲取元素的src屬性
                except NoSuchElementException:                                          # 如果找不到元素
                    continue                                                            # 繼續下一次迴圈
        data.append(photo_url)                                                          # 將photo_url添加到data列表中

        print("目前載入 : ",len(data),"/",len(area))                                     # 輸出當前載入的數量和area列表的長度
    print("載入完成-開始下載")                                                            # 輸出完成載入的信息
    driver.quit()                                                                       # 關閉瀏覽器驅動實例
                                                                     

    x = 1                                                                               # 初始化變數x為1

    for line in data:                                                                   # 迴圈遍歷data列表
        if not os.path.exists(seach):                                                   # 如果seach目錄不存在
            os.makedirs(seach)                                                          # 創建seach目錄

        try:                                                                            # 嘗試執行以下代碼
            w = requests.get(line)                                                      # 發送GET請求並獲取響應
        except requests.exceptions.RequestException as e:                               # 如果發生RequestException異常
            print(f"無法下載圖片 {line}: {e}")                                           # 輸出異常信息
            continue                                                                    # 繼續下一次迴圈
    
        if '.gif' in line:                                                              # 如果line中包含'.gif'
            file = str(x) + '.gif'                                                      # 設置file為x.gif
        else:                                                                           # 否則
            file = str(x) + '.jpg'                                                      # 設置file為x.jpg

        with open (seach + '/' + file , 'wb') as fObj:                                  # 打開文件並寫入二進制數據
            fObj.write(w.content)                                                       # 寫入響應內容
            x += 1                                                                      # x增加1
            time.sleep(1)                                                               # 等待1秒
        print(line)                                                                     # 輸出line


seach = input("請輸入搜尋內容 : ")                                                        # 獲取用戶輸入並設置為seach
area  = LINK(seach)                                                                     # 調用LINK函數並設置返回值為area
PHOTO(area, seach)                                                                      # 調用PHOTO函數


seach = input("請輸入搜尋內容 : ")                                                      
area  = LINK(seach)                                                                   
PHOTO(area, seach)      




