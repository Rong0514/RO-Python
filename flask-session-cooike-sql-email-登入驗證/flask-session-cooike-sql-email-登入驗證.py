# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 20:29:41 2023

@author: willy
"""

from flask import Flask
from flask import request
from flask import session
from flask import make_response
from flask import render_template
from flask_mail import Mail, Message
import sqlite3
import os 
import webbrowser

app = Flask(__name__)

global sendemail
sendemail    = input("請輸入寄出信箱 : ")
app_password = input("應用程式密碼")

app.config['MAIL_SERVER']   = 'smtp.gmail.com'
app.config['MAIL_PORT']     = 465
app.config['MAIL_USERNAME'] = sendemail 
app.config['MAIL_PASSWORD'] = app_password  
app.config['MAIL_USE_TLS']  = False
app.config['MAIL_USE_SSL']  = True
mail = Mail(app)

app.secret_key = 'Rong secret key'

db_name        = 'sginup.db'
db_exists      = os.path.exists(db_name)
conn = sqlite3.connect('sginup.db')
if db_exists  == True:
    print("Database file exists, opened successfully.")
else:
    print("Database file doesn't exist, created successfully.")
    sql = "CREATE TABLE 'rong' ('ID' INTEGER PRIMARY KEY AUTOINCREMENT, 'name' TEXT, 'birthday' TEXT, 'sex' TEXT, 'email' TEXT, 'user' TEXT, 'password' TEXT, 'verify' TEXT);"
    conn.execute(sql)
    conn.commit()
conn.close()

@app.route("/home") 
def Home():
    return render_template("home.html") 

@app.route("/login", methods = ['GET', 'POST'])
def login():
    
    if  request.method == 'POST':
        session['email']    = request.form.get('email')
        session['user']     = request.form.get('user')
        session['password'] = request.form.get('password')
        
        resp = make_response(render_template("login_successfully.html"))
        resp.set_cookie('userID'  , session['user'])
        resp.set_cookie('emailID' , session['email'])
        return resp
    
    elif 'user' in session and 'password' in session and session.get("logined") == "1":
        return render_template("login_successfully.html")
    
    else:
        user  = request.cookies.get('userID')  
        email = request.cookies.get('emailID') 
        return render_template('login_form.html', user = user , email = email)


@app.route('/login_form' ,  methods = ['GET', 'POST'])
def login_form():
    
    if request.method == 'POST':
        email    = request.form.get('email')
        user     = request.form.get('user')
        password = request.form.get('password')
        
        conn     = sqlite3.connect('sginup.db')
        cursor   = conn.cursor()
        sql      = "select * from rong where user = ? and password = ?"
        cursor.execute(sql, (user , password))
        data     = cursor.fetchone()
        
        if data != None:
            conn     = sqlite3.connect('sginup.db')
            cursor   = conn.cursor()
            sql      = "select * from rong where email = ?"
            cursor.execute(sql, (email,))
            data     = cursor.fetchone()
            if data != None:
                sql  = "select verify from rong where user=? and password=?"
                cursor.execute(sql, (user,password))
                data = cursor.fetchone()
    
                if data[0] == '已驗證':
                    session['email']    = email
                    session['user']     = user
                    session['password'] = password
                    session["logined"]  = "1" 
                    
                    resp = make_response(render_template("login_successfully.html"))
                    resp.set_cookie('userID'  , user)
                    resp.set_cookie('emailID' , email)
                    return resp
                
                else:
                    return render_template('verifyfail.html')
            else:
                 return "<h1>信 箱 尚 未 註 冊</h1> <br> <p><a href = '/login'>重 新 登 入</a></p>"               
        else:
            return "<h1>帳 號 或 密 碼 錯 誤</h1> <br> <p><a href = '/login'>重 新 登 入</a></p>"
    else:
        return "<h1>您 尚 未 註 冊 </h1> <br> <p><a href = '/sginup_form'>註 冊</a></p>"
    
    conn.close()


@app.route('/sginup_form')
def sginup_form():
    return render_template('sginup_form.html')

@app.route("/trysginup" , methods = ['POST'])
def trysginup():
    
    if request.method == 'POST' :
            name      = request.form['name']
            birthday  = request.form['birthday']
            sex       = request.form['sex']
            email     = request.form['email']
            user      = request.form['user']
            password  = request.form['password']
            verify    = '未驗證'
            try:
                with sqlite3.connect('sginup.db') as conn:
                     cursor = conn.cursor()
                     sql = "select * from rong where email='{}'".format(email)
                     cursor.execute(sql)
                     conn.commit()
                     result = cursor.fetchone()
                     if result is None or result[4] is None:
                        try:
                            with sqlite3.connect('sginup.db') as conn:
                                 cursor = conn.cursor()
                                 sql = "insert into 'rong' (name,birthday,sex,email,user,password,verify) values('{}','{}','{}','{}','{}','{}','{}')".format(name , birthday , sex , email , user , password , verify)
                                 cursor.execute(sql)
                                 conn.commit()
                                 msg = 'sginup successfully.'
                                 response = render_template("sginup_successfully.html",msg=msg,name=name,birthday=birthday,email=email,sex=sex,user=user,password=password,verify=verify)
                                 return response
                        except:
                                conn.rollback()
                                return "<h1>error in insert operation.1</h1>"
                     else:
                         return "<h1>error in insert operation</h1> <br> <h1>此信箱已被註冊 請重新註冊</h1> <br> <a href='/sginup_form'>重 新 註 冊</a>"
            except:
                    conn.rollback()
                    return "<h1>error in insert operation.2</h1>"
            finally:
                conn.close()

@app.route("/verify")
def verify():
    return render_template("verify_form.html")

@app.route("/sendverify", methods = ['POST'])
def sendverify():

    email    = request.form['email']
    msg      = Message('驗 證', sender = sendemail , recipients = [email])
    msg.html = render_template('verify.html' , email = email)  #驗證畫面     
    mail.send(msg)
    return render_template('sendemail.html') #給予前往驗證連結

@app.route('/getverify', methods = ['GET'])
def getverify():
    email = request.args.get('email')
    
    try:
        with sqlite3.connect('sginup.db') as conn:
              cursor  = conn.cursor()
              sql     = "select * from rong where email='{}'".format(email)
              cursor.execute(sql)
              result  = cursor.fetchone()
              if result is not None and result[4] == email:
                  sql = "update rong set verify='已驗證' where email='{}'".format(email)
                  cursor.execute(sql)
                  conn.commit()
                  return render_template('verifysuccessfully.html')
              else:
                  return render_template('verifyfail.html')
    except:
        return render_template('verifyfail.html')
    
    finally:
        conn.close()

@app.route("/successfully")
def successfully():
    return render_template("login_successfully.html")

@app.route("/logout")                 
def logout():
    session.pop('email'    , None)   
    session.pop('user'     , None)  
    session.pop('password' , None)
    return render_template('home.html')

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/home")
    app.run(debug = False)

