# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:21:46 2023

@author: willy
"""

from bs4 import BeautifulSoup
import requests
from flask import Flask

app = Flask(__name__)

@app.route("/lotto")
def lotto():
    numbers = []  # 建立一個空的列表來儲存號碼
    for year in range(110,111):
        for month in range(1,3):
            lottoUrl='http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
            
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
                numbers.append(resData[i].text)  # 將號碼添加到列表中
    print("lotto已經都抓完囉") 
    return ', '.join(numbers)  # 將號碼列表轉換為字符串並返回

@app.route("/cola/<seach>")
def Cola(seach):
    results = []  # 建立一個空的列表來儲存結果
    session = requests.session()                                          
    url1    = 'https://www.colatour.com.tw/'                                 
    header  = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
              }                                                              
    data    = session.get(url1 , headers = header)                       
    p1 = 'DepartureCity=*'                                                   
    p2 = 'KeyWord={}'.format(seach)
    p3 = 'Source=00'
    url2    = 'https://www.colatour.com.tw/C10A_TourSell/C10A08_PatternSearch.aspx?{}&{}&{}'.format(p1,p2,p3)
    payload = {                                                              
                'DepartureCity': '*',
                'KeyWord': seach,
                'Source': '00'
                  }  
    data    = session.get(url2 , headers = header , params = payload)         
    soup    = BeautifulSoup(data.text , 'html.parser')                       
    total   = soup.select('ul.tourin-city-list-block li')
    
    for row in total:
        title = row.select_one('div.tourin-city-list-name p')
        links = row.select_one('div.tourin-city-list-nameblock a')
        photos= row.select_one('div.pattern-imgpush a img')
        price = row.select_one('div.tourin-city-list-price p')
        
        if title != None:
            link  = links.get('href')
            photo = photos.get('src') 
            results.append("標題: " + title.text)
            results.append("連結: " + 'https://www.colatour.com.tw'+link)
            results.append("圖片: " + photo)
            results.append("價格: " + price.text)
    return '<br>'.join(results)  # 將結果列表轉換為字符串並返回

app.run(debug=False)
