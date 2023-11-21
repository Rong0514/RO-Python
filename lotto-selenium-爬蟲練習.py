# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:14:58 2023

@author: willy
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time


browser = webdriver.Chrome()                                                   # 建立瀏覽器物件

browser.implicitly_wait(10)                                                    # 隱性等待，最長等10秒

browser.get('https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx')    # 使用driver 抓取網址

select  = Select(browser.find_element(By.NAME,'forma'))                         # 找到下拉式選單
select.select_by_visible_text(u'大樂透')                                        # 指定內文(u = 編碼)

browser.find_element(By.ID,'Lotto649Control_history_radYM').click()            # 點擊ID(點擊選項)

for i in range(103,112):
    select = Select(browser.find_element(By.ID,'Lotto649Control_history_dropYear'))# 找到下拉式選單(年份)
    n1     = str(i)
    select.select_by_value(n1)
    
    
    for i in range(1,13):
        select = Select(browser.find_element(By.ID,'Lotto649Control_history_dropMonth'))# 找到下拉式選單(月份)
        n2     = str(i)
        select.select_by_value(n2)
        
        
        browser.find_element(By.ID,"Lotto649Control_history_btnSubmit").click()# 點擊(查詢)
        
        data   = browser.page_source
        
        time.sleep(3)                                                          # 強制等待3秒再執行下一步
        
        
        
        soup   = BeautifulSoup(data,'html.parser')
  
        good   = soup.select_one('table',id='Lotto649Control_history_dlQuery')
        trss   = good.find_all('tr')[0]
        table  = trss.find('table',class_='table_org td_hm')
        
        
        dates  = table.find_all('tr')[1]
        date   = dates.find('span' , id='Lotto649Control_history_dlQuery_L649_DDate_0')
        print(date.text)
        
        trs    = table.find_all('tr')[4]
        title = trs.find('td' ,class_="td_org2")
        print(title.text.strip() + ': ' , end='')
        
        
        tds    = trs.find_all('td',class_='td_w font_black14b_center')
        for td in tds:
            print(td.text,end=' ')
            red = soup.find('span',id = 'Lotto649Control_history_dlQuery_No7_0')
        print()
        print('特 別 號 : '+red.text)
        print()
        
        
browser.close()



