# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 15:33:13 2023

@author: willy
"""

from flask import Flask,render_template,request,redirect,url_for               #連接到這個template檔案
import db
from flask_paginate import Pagination,get_page_parameter                       # 分頁
from datetime import datetime


app = Flask(__name__)                                                          #建立Flask物件初始化設定

@app.route('/home')

def HOME():                                                                    # 首頁
    
    sql = "select title,link_url,photo_url,star from jpfoods where platform = '大阪' order by star desc limit 13"
    db.cursor.execute(sql)
    jpfoods = db.cursor.fetchall()
    
    sql = "select title,link_url,photo_url from ifoods where platform = '愛食記' order by id asc limit 10"
    db.cursor.execute(sql)
    ifoods1 = db.cursor.fetchall()
    
    sql = "select title,link_url,photo_url from ifoods where platform = '愛食記' order by id desc limit 11"
    db.cursor.execute(sql)
    ifoods2 = db.cursor.fetchall()
    
    sql = "select title,link_url,photo_url from travel where platform = '東京' order by id asc limit 12"
    db.cursor.execute(sql)
    travel = db.cursor.fetchall()
    
    return render_template('HOME.html',**locals())


@app.route('/ifoods')

def ifoods():
    
    page = int(request.args.get('page',1))
    
    sql = "select count(*) as c from ifoods"                                   # 查找共有多少筆數
    
    db.cursor.execute(sql)
    
    datacount = db.cursor.fetchone()                                           # 指找尋一筆最上層
    
    count = int(datacount[0])
    
    if page == 1:
        sql  = "select title,link_url,photo_url,address from ifoods order by id desc limit 20"
        
    else:
        startp = page-1
        sql  = "select title,link_url,photo_url,address from ifoods limit {},{}".format(startp*20,20)
                                                                                # 頁數*36 = 初始筆數
    db.cursor.execute(sql)
    
    ifood = db.cursor.fetchall()#fetchall(抓取全部的資料)
    
    pagination = Pagination (page = page, total = count , per_page = 20)
                   # 使用函式    頁數           總比數          以20筆為分頁

    return render_template('ifoods.html',**locals())


@app.route("/jpfoods")

def jpfoods():
    
    p = request.args.get('p', '')
    
    if len(p) == 0:
        sql = "select title,link_url,photo_url,star from jpfoods order by star desc"
    else:
        sql = "select title,link_url,photo_url,star from jpfoods where platform = '{}'".format(p)
        
    db.cursor.execute(sql)
    jpfood = db.cursor.fetchall()
    return render_template("jpfoods.html", **locals())



@app.route("/travel")

def travel():
    
    p = request.args.get('p', '')
    
    page = int(request.args.get('page',1))
    
    sql = "select count(*) as c from travel"                                   # 查找共有多少筆數
    
    db.cursor.execute(sql)
    
    datacount = db.cursor.fetchone()                                           # 指找尋一筆最上層
    
    count = int(datacount[0])

    if  page == 1 and p == '':
        if len(p) == 0:
            sql = "select title,link_url,photo_url,platform from travel order by id asc limit 20"
            
        else:
            sql = "select title,link_url,photo_url,platform from travel where platform = '{}' order by id asc limit 20".format(p)
        
    else: 
        startp = page-1
        if len(p) == 0:

            sql = "select count(*) as c from travel "
                
            db.cursor.execute(sql)
                
            datacount = db.cursor.fetchone()                                   # 指找尋一筆最上層
                
            count = int(datacount[0])  
            
            print('page:',count)
            
            sql = "select title,link_url,photo_url,platform from travel order by id asc limit {},{}".format(startp*20,20)
            
        else:
            
            sql = "select count(*) as c from travel where platform = '{}'".format(p)
                
            db.cursor.execute(sql)
                
            datacount = db.cursor.fetchone()                                   # 指找尋一筆最上層
                
            count = int(datacount[0]) 
            print(count)
            
            sql = "select title,link_url,photo_url,platform from travel where platform = '{}' order by id asc limit {},{}".format(p,startp*20,20)
        
    db.cursor.execute(sql)
    
    travels = db.cursor.fetchall()
    
    count = int(datacount[0])
    
    pagination = Pagination (page = page, total = count , per_page = 20)
                    # 使用函式    頁數           總比數          以20筆為分頁
    return render_template("travel.html", **locals())

@app.route('/contact')

def message():
    return render_template('message.html')



@app.route("/addcontact",methods = ['POST'])           #methods = 多個方法
def contact():
    
    if request.method == "POST" :                      # 如果送出的方法是post才進入
    
        username = request.form.get('name')
        email    = request.form.get('email')
        title    = request.form.get('title')
        content  = request.form.get('content')
        today    = datetime.today()
        c_date   = datetime.strftime(today,'%Y-%m-%d') #時間轉文字

        sql = "insert into contact(subject,name,email,content,create_date) values('{}','{}','{}','{}','{}')".format(title,username,email,content,c_date)
                                        #  欄  位  名  稱                                                                     變  數  名  稱
        db.cursor.execute(sql)          #執行
        db.conn.commit()                #馬上回傳
        
    return redirect(url_for('message'))


app.run(debug=False)


