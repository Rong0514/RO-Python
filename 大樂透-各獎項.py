# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 20:31:29 2023

@author: USER
"""
import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
    
url    = 'https://www.taiwanlottery.com.tw/index_new.aspx'

data   = requests.get(url,headers = header).text

soup   = BeautifulSoup(data,'html.parser')

ID     = soup.find(id ='rightdown')

print('<!--*************************************************BINGO BINGO-->')
print()
box01   = ID.find("div",class_='contents_box01')
title   = box01.find("span",class_='font_black15')
red14   = box01.find('span',class_='font_red14')
lis     = red14.find_all('a')
link    = []
for row in lis:
    lin = row.get('href')
    link.append(lin)
link1   = '開獎結果: https://www.taiwanlottery.com.tw'+link[0]
link2   = '獎號查詢: https://www.taiwanlottery.com.tw'+link[1]
number  = box01.find_all('div',class_='ball_tx ball_yellow')
data    = []
for row in number:
    data.append(row.text)
sup     = box01.find('div',class_='ball_red')
Gue     = box01.find('div',class_= 'ball_blue_BB1')
mxm     = box01.find('div',class_='ball_blue_BB2')
print(title.text)
print(link1) ; print(link2)
print('開出獎號: '+' '.join(data))
print('超級獎號: '+sup.text) 
print('猜 大 小: '+Gue.text)
print('猜 單 雙: '+mxm.text)


print()
print('<!--***************************************************雙贏彩區塊-->')
print()
box06  = ID.find("div",class_='contents_box06')
title  = box06.find('span',class_='font_black15')
lis    = box06.find('span',class_='font_red14')
link   = lis.find('a').get('href')
number = box06.find_all('div',class_='ball_tx ball_blue')
data   = []
for row in number:
    data.append(row.text)
    
print(title.text)
print('開獎連結: https://www.taiwanlottery.com.tw'+link)
print('開出獎號: '+' '.join(data[0:12]))
print("開獎順序: "+' '.join(data[12:]))


print()
print('<!--***************************************************威力彩區塊-->')
print()
box02 = ID.find_all('div',class_='contents_box02')
a      = box02[0]
title  = a.find('span',class_='font_black15')
lis    = a.find('span',class_='font_red14')
link   = lis.find('a').get('href')
number = a.find_all('div',class_='ball_tx ball_green')
data   = []
for row in number:
    data.append(row.text)
spa    = a.find('div',class_='ball_red')

print(title.text)
print('開獎連結: https://www.taiwanlottery.com.tw'+link)
print('開出獎號: '+' '.join(data[0:6]))
print("開獎順序: "+' '.join(data[6:]))
print("第 二 區: "+ spa.text)


print()
print("<!--*************************************************38樂合彩區塊-->")
print()

a      = box02[1]
title  = a.find('span',class_='font_black15')
lis    = a.find('span',class_='font_red14')
link   = lis.find('a').get('href')
number = a.find_all('div',class_='ball_tx ball_green')
data   = []
for row in number:
    data.append(row.text)
    
print(title.text)
print('開獎連結: https://www.taiwanlottery.com.tw'+link)
print('開出獎號: '+' '.join(data[0:6]))
print("開獎順序: "+' '.join(data[6:]))

print()
print('<!--***************************************************大樂透區塊-->')
print()

a      = box02[2]
title  = a.find('span',class_='font_black15')
lis    = a.find('span',class_='font_red14')
link   = lis.find('a').get('href')
number = a.find_all('div',class_='ball_tx ball_yellow')
data   = []
for row in number:
    data.append(row.text)
spa    = a.find('div',class_='ball_red')

print(title.text)
print('開獎連結: https://www.taiwanlottery.com.tw'+link)
print('開出獎號: '+' '.join(data[0:6]))
print("開獎順序: "+' '.join(data[6:]))
print('特 別 號: '+spa.text)

print()
print('<!--*************************************************49樂合彩區塊-->')
print()

a      = box02[3]
title  = a.find('span',class_='font_black15')
lis    = a.find('span',class_='font_red14')
link   = lis.find('a').get('href')
number = a.find_all('div',class_='ball_tx ball_yellow')
data   = []
for row in number:
    data.append(row.text)
    
print(title.text)
print('開獎連結: https://www.taiwanlottery.com.tw'+link)
print('開出獎號: '+' '.join(data[0:6]))
print("開獎順序: "+' '.join(data[6:]))

print()
print('<!--**************************************************今彩539區塊-->')
print()

box03  = ID.find_all('div',class_='contents_box03')
a      = box03[0]
title  = a.find('span',class_='font_black15')
lis    = a.find('span',class_='font_red14')
link   = lis.find('a').get('href')
number = a.find_all('div',class_='ball_tx ball_lemon')
data   = []
for row in number:
    data.append(row.text)
    
print(title.text)
print('開獎連結: https://www.taiwanlottery.com.tw'+link)
print('開出獎號: '+' '.join(data[0:5]))
print("開獎順序: "+' '.join(data[5:]))

print()
print('<!--*************************************************39樂合彩區塊-->')
print()

a      = box03[1]
title  = a.find('span',class_='font_black15')
lis    = a.find('span',class_='font_red14')
link   = lis.find('a').get('href')
number = a.find_all('div',class_='ball_tx ball_lemon')
data   = []
for row in number:
    data.append(row.text)
    
print(title.text)
print('開獎連結: https://www.taiwanlottery.com.tw'+link)
print('開出獎號: '+' '.join(data[0:5]))
print("開獎順序: "+' '.join(data[5:]))

print()
print('<!--****************************************************3星彩區塊-->')
print()

box04  = ID.find_all('div',class_='contents_box04')
a      = box04[0]
title  = a.find('span',class_='font_black15')
lis    = a.find('span',class_='font_red14')
link   = lis.find('a').get('href')
number = a.find_all('div',class_='ball_tx ball_purple')
data   = []
for row in number:
    data.append(row.text)
    
print(title.text)
print('開獎連結: https://www.taiwanlottery.com.tw'+link)
print('開出獎號: '+' '.join(data))

print()
print('<!--****************************************************4星彩區塊-->')
print()

a      = box04[1]
title  = a.find('span',class_='font_black15')
lis    = a.find('span',class_='font_red14')
link   = lis.find('a').get('href')
number = a.find_all('div',class_='ball_tx ball_purple')
data   = []
for row in number:
    data.append(row.text)
    
print(title.text)
print('開獎連結: https://www.taiwanlottery.com.tw'+link)
print('開出獎號: '+' '.join(data))


print()