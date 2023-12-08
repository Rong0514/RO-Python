# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 15:03:13 2023

@author: willy
"""

import threading  # 導入threading模組
import time       # 導入time模組
import random     # 導入random模組
import queue      # 導入queue模組

Done_time = queue.Queue()  # 創建一個隊列來存儲完成時間

# 建立一個全域的鎖物件
print_lock = threading.Lock()

def Playground5(name):                       # 定義Playground5函數
    sleep_time = random.randint(0, 1)        # 生成一個隨機的睡眠時間
    time.sleep(sleep_time)                   # 讓當前執行緒暫停一段時間
    Done_time.put((name, int(time.time())))  # 將選手的名字和完成時間添加到隊列中
    with print_lock:                         # 獲取鎖
        print(name + ' - 5 完成比賽！')       # 打印選手完成比賽的消息

def Playground4(name):
    sleep_time = random.randint(0, 1)
    time.sleep(sleep_time)
    with print_lock:
        print(name + ' - 4 棒起跑')
    t4 = threading.Thread(target = Playground5 , args = (name,)) 
    t4.start()
    t4.join()

def Playground3(name):
    sleep_time = random.randint(0, 1)
    time.sleep(sleep_time)
    with print_lock:
        print(name + ' - 3 棒起跑')
    t3 = threading.Thread(target = Playground4 , args = (name,)) 
    t3.start()
    t3.join()
    
def Playground2(name):
    sleep_time = random.randint(0, 1)
    time.sleep(sleep_time)
    with print_lock:
        print(name + ' - 2 棒起跑')
    t2 = threading.Thread(target = Playground3 , args = (name,)) 
    t2.start()
    t2.join()
    
def Playground1(name):
    sleep_time = random.randint(0, 1)
    time.sleep(sleep_time)
    with print_lock:
        print(name + ' - 1 棒起跑')
    t1 = threading.Thread(target = Playground2 , args = (name,)) 
    t1.start()
    t1.join()

threads = []           # 創建一個列表來存儲所有的執行緒
for i in range(1,6):   # 對於每一個選手
    t = threading.Thread(target = Playground1 , args = ("選手:"+str(i),))  # 創建一個新的執行緒來執行Playground1函數
    t.start()          # 開始執行新的執行緒
    threads.append(t)  # 將新的執行緒添加到列表中

for t in threads:      # 對於列表中的每一個執行緒
    t.join()           # 等待該執行緒結束

Donetime = sorted(list(Done_time.queue), key=lambda x: x[1])  # 將隊列轉換為列表，並根據完成時間進行排序
rank = 1               # 初始化名次
print()
for i in Donetime:     # 對於每一個選手
    with print_lock:   # 獲取鎖
        print(i[0] + " 第 " + str(rank) + " 名")  # 打印選手的名次
    rank += 1          # 名次加一

with print_lock:       # 獲取鎖
    print("Done.")     # 當所有執行緒都結束後，打印 "Done."
