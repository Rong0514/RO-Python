# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:08:43 2023

@author: willy
"""

import threading
from bs4 import BeautifulSoup
import requests
import os

# 子執行緒的工作函數
def lotto():
    for year in range(111,112):
        for month in range(1,13):
            lottoUrl='http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
            #res = requests.get(lottoUrl)
            
            res = requests.get(lottoUrl)
            soup = BeautifulSoup(res.text,'html.parser')
            
            VIEWSTATE=soup.select_one("#__VIEWSTATE")["value"]
            VIEWSTATEGENERATOR=soup.select_one("#__VIEWSTATEGENERATOR")["value"]
            EVENTVALIDATION=soup.select_one("#__EVENTVALIDATION")["value"]                
            
            payLoad={'__EVENTTARGET':'',
                    '__EVENTARGUMENT':'',
                    '__LASTFOCUS':'',
                    '__VIEWSTATE':VIEWSTATE,
                    '__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR,
                    '__EVENTVALIDATION':EVENTVALIDATION,
                    'Lotto649Control_history$DropDownList1':'2',
                    'Lotto649Control_history$chk':'radYM',
                    'Lotto649Control_history$dropYear':year,
                    'Lotto649Control_history$dropMonth':month,
                    'Lotto649Control_history$btnSubmit': '查詢'}
            
            res = requests.post(lottoUrl, data=payLoad)
            
            soup = BeautifulSoup(res.text,'html.parser')
            
            testList = ['Lotto649Control_history_dlQuery_No1_0',
                        'Lotto649Control_history_dlQuery_No2_0',
                        'Lotto649Control_history_dlQuery_No3_0',
                        'Lotto649Control_history_dlQuery_No4_0',
                        'Lotto649Control_history_dlQuery_No5_0',
                        'Lotto649Control_history_dlQuery_No6_0',
                        'Lotto649Control_history_dlQuery_No7_0']
            
            resData = soup.find_all(id=testList)
            for i in range(len(resData)):
                print(resData[i].text)  
    print("lotto已經都抓完囉") 
    
def ptt(keyword, count):
    pics = []
    picCount = 0   
    
    r = requests.Session()
    payload ={
        "from":"/bbs/Beauty/index.html",
        "yes":"yes"
    }    
    r.post("https://www.ptt.cc/ask/over18?from=%2Fbbs%2FBeauty%2Findex.html",payload)
    
    url = "https://www.ptt.cc/bbs/Beauty/index.html"    
    os.makedirs(keyword)
    
    while True:
        title = []
        titleUrl = []
        r2 = r.get(url)
        soup = BeautifulSoup(r2.text,"html.parser")
        
        sel = soup.select("div.title a") #標題
        u = soup.select("div.btn-group.btn-group-paging a") #a標籤   
        url = "https://www.ptt.cc"+ u[1]["href"] #上一頁的網址
        
        for s in sel: #
            if keyword in s.text:
                #帥哥 正妹 新垣結衣"
                title.append(s.text)
                titleUrl.append(s["href"])            
                #print(s["href"],s.text)
    
        for i in range(len(titleUrl)):
            url2 = "https://www.ptt.cc"+titleUrl[i]
            r3 = r.get(url2)
            soup = BeautifulSoup(r3.text,"html.parser")
            sel2 = soup.select("a") 
            
            for s in sel2: 
                picUrl=s["href"]
                if "jpg" in picUrl or "gif" in picUrl or "png" in picUrl:
                    pics.append(picUrl)
                    resp2 = r.get(picUrl)
                    if resp2.status_code == 200:
                        with open(keyword+'/'+str(pics.index(picUrl)+1)+picUrl[-4:], 'wb') as f:
                            for chunk in resp2:
                                f.write(chunk)  
                            picCount = picCount +1
                if picCount==count:
                    print("--------------------------------------------")
                    print("ptt已經都抓完囉")
                    return  
                
t1 = threading.Thread(target = lotto)
t2 = threading.Thread(target = ptt, args = ('正妹', 100))

t1.start()
t2.start()

t1.join()
t2.join()

print("Done.")




    
    
    
    
    