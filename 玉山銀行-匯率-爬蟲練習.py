# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 23:08:10 2023

@author: willy
"""

import requests
from bs4 import BeautifulSoup

url   = 'https://www.esunbank.com/zh-tw/personal/deposit/rate/forex/foreign-exchange-rates'# 請求網址

data  = requests.get(url).text                                                 # 將網址requests.get方式送回去

soup  = BeautifulSoup(data, 'html.parser')                                     # 帶入BeautifulSoup 用 html.parser解析 

tbody = soup.find('tbody',class_ = 'l-exchangeRate__table result')

trs   = tbody.find_all('tr',recursive = False)[1:]

for row in trs:
    tds = row.find_all('td',recursive = False)
    if len(tds) == 4:
        print(tds[0].text.strip().split()[0])
        print(tds[1].text.strip())
        print(tds[2].text.strip())
        print(tds[3].text.strip())
