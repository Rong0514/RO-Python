# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 19:33:31 2023

@author: USER
"""

'''

安裝軟件:tesseract-ocr-w64-setup-v5.0.0- _________確認執行檔位置

________________pip install pytesseract__

________________pip install pillow__

________________pip install Image__


'''

from bs4 import BeautifulSoup

import requests

from PIL import Image

import pytesseract


def compute(city,area,street):
    while True:
        
        session = requests.Session()                                           # 以session方式做保持連接(紀錄 點擊、登陸)
                
        header  = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
                    }                                                          # 瀏覽器代理用戶(標頭)
        
        url     = 'https://www.post.gov.tw/post/internet/Postal/index.jsp?ID=208' # 請求網址


        '''________________________________傳送第一次請求__進入網頁________________________________'''  
         
        data    = session.get(url,headers=header)                              # 將網址、標頭以session.get方式送回去
        
        soup    = BeautifulSoup(data.text,'html.parser')                       # data帶入BeautifulSoup解析(用html.parser方式)
         
        vkey    = soup.select_one("input#vKey").get("value")                   # payload 需要 因為在第一順位所以用select_one
        
        
        '''________________________________驗證碼________________________________'''
        
        number  = soup.select_one("img#imgCaptcha3_zip6").get('src')[3:]       # 抓取驗證碼開頭有../所以從索引值3開始讀取
        
        numurl  = "https://www.post.gov.tw/post/internet/" + number            # 將完整網址帶給變數
        
        '''________________________________傳送第二次請求__進入驗證碼________________________________'''  
        
        data    = session.get(numurl , headers = header)                       # 將驗證碼網址、標頭以session.get方式送回去
        
        if data.status_code == 200:                                            # 如果HTTP 狀態碼  == 200時才進入(代表一切正常) 
            with open('ans.jpg','wb') as file:                                 # 以複寫方式寫入
                for photo in data: 
                    file.write(photo)                                          # 將photo寫入file
            
        pytesseract.pytesseract.tesseract_cmd=r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #OCR執行黨位置
        
        img    = Image.open('ans.jpg')                                         # 使用Image函式開啟驗證碼圖片檔
        
        img    = img.convert('L')                                              # 將圖片處理成灰度(提高辨識度)
        
        ans    = str.strip(pytesseract.image_to_string(img,config ='--psm 6')) 
                                      # 以文字型態並去除前後空白使用pytesseract.image_to_string解析(變數 , 頁面分段模式'--psm 6')
        
        # print(ans)
        
        '''________________________________將蒐集完的訊息帶進payload________________________________'''     
        
        payload = { 
                    "list":"5",
                    "list_type": "1",
                    "firstView": "3",
                    "vKey": vkey,
                    "city_zip6": city,
                    "cityarea_zip6": area,
                    "street_zip6": street,
                    "checkImange_zip6": ans,
                    "Submit": "查詢" 
                    }
        
        print("查詢中")
        
        '''________________________________傳送第三次請求__進入搜尋結果________________________________'''  
        
        url3      = "https://www.post.gov.tw/post/internet/Postal/index.jsp?ID=208" # 請求網址
        
        data      = session.post(url3 , headers = header ,  data = payload)    # 將網址、標頭、payload以session.post方式送回去
        if data.status_code==200:                                              # 如果HTTP 狀態碼  == 200時才進入(代表一切正常) 
            
            if "驗證碼輸入錯誤" in data.text:                                    # 如果字串在標題裡面 >>> 跳下一個敘述
                # print("驗證碼錯誤，重試一遍")
                continue
            
            else:
                soup  = BeautifulSoup(data.text,"html.parser")                 # data帶入BeautifulSoup解析(用html.parser方式)
                
                zip1  = soup.find_all("td", attrs={"data-th":"郵遞區號"})       
                zip2  = soup.find_all("td", attrs={"data-th":"區域"})
                zip3  = soup.find_all("td", attrs={"data-th":"路名"})           
                zip4  = soup.find_all("td", attrs={"data-th":"段號"})           
                zip5  = soup.find_all("td", attrs={"data-th":"投遞範圍"})  
                zip6  = soup.find_all("td", attrs={"data-th":"大宗段名稱"}) 
                
                for zipa,zipb,zipc,zipd,zipe,zipf in zip(zip1,zip2,zip3,zip4,zip5,zip6):
                    print(zipa.text,
                          zipb.text,
                          zipc.text,
                          zipd.text,
                          zipe.text,
                          zipf.text
                          )
        break
    
    
    
    
city     = input("請輸入想搜尋的縣市：")
area     = input("請輸入想搜尋的鄉鎮[市]區：")
street   = input("請輸入想搜尋的路(街)名或鄉里：")
compute(city, area, street)


 
