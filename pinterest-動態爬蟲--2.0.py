# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 10:20:44 2023

@author: willy
"""

from selenium import webdriver                                              
from selenium.webdriver.common.by import By                                 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC                            
import time                                                                
from bs4 import BeautifulSoup                                              
import requests                                                             
import os                                                                   
from selenium.common.exceptions import NoSuchElementException               


def LINK(seach):                                                           
    driver = webdriver.Chrome()                                           
    driver.implicitly_wait(3)                                              
    driver.get("https://www.pinterest.jp/ideas/")                         
    driver.find_element(By.CSS_SELECTOR , "div.ujU.zI7.iyn.Hsu input").send_keys(seach + Keys.ENTER)  
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))                                                     
    
    area      = []                                                              
    
    for i in range(4):
        data  = driver.page_source                                          
        soup  = BeautifulSoup(data , 'html.parser')                          
        links = soup.select('div[data-test-id=deeplink-wrapper] a')        
        
        for row in links:                                                   
            href = 'https://www.pinterest.jp' + row.get('href')            
            if href not in area:                                           
                area.append(href)                                          
                
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)') 
        time.sleep(2)                                                      
        
    driver.quit()                                                          
    print("總共 : ",len(area),'筆')                                        
    
    return area                                                             



def PHOTO(area, seach):                                                                 
    driver = webdriver.Chrome()                                                         
    data   = []                                                                          
    driver.implicitly_wait(3)                                                         
    for i in area:                                                                   
        driver.get(i)                                                                   
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))                                                               
        body_text = driver.find_element(By.TAG_NAME, "body").text                     
        if "內容創作者已移除這個內容" in body_text:                                    
            continue                                                                  
        try:                                                                            
            video     = driver.find_element(By.CSS_SELECTOR , 'div.iCM.XiG.L4E.o5r video') 
            photo_url = video.get_attribute('poster')                                 
        except NoSuchElementException:                                                
            try:                                                                    
                videos    = driver.find_element(By.CSS_SELECTOR , 'div[data-test-id=story-pin-closeup] img')  
                photo_url = videos.get_attribute('src')                                 
            except NoSuchElementException:                                            
                try:                                                                    
                    photo     = driver.find_element(By.CSS_SELECTOR , 'div[data-test-id=pin-closeup-image] img') 
                    photo_url = photo.get_attribute('src')                             
                except NoSuchElementException:                                        
                    continue                                                          
        data.append(photo_url)                                                       
        
        print("目前載入 : ",len(data),"/",len(area))                                    
    print("載入完成-開始下載")
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
            
        if '.gif' in line:                                                            
            file = str(x) + '.gif'                                                    
        else:                                                                          
            file = str(x) + '.jpg'                                                     
        
        with open (seach + '/' + file , 'wb') as fObj:                                
            fObj.write(w.content)                                                     
            x += 1                                                                    
            time.sleep(1)                                                             
        print(line)                                                                     


seach = input("請輸入搜尋內容 : ")                                                      
area  = LINK(seach)                                                                   
PHOTO(area, seach)                                                                     
