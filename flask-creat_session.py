# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 21:37:37 2023

@author: willy
"""

from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import url_for
import webbrowser

app = Flask(__name__)
app.secret_key = 'Rong secret key'

@app.route('/home')
def home():
    if 'username' in session and 'password' in session and session['logined']=='1':
        username = session['username']
        password = session['password']
        return '登入使用者名稱是:' + username + '<br>' +\
               '登入使用者密碼是:' + password + '<br>' +\
               "<b><a href = '/logout'>點選這裡登出</a></b>"
    else:
        return "您尚未登入， <br><a href = '/login'></b>" + '點選這裡登入</b></a>'

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]
        session["logined"]  = "1"
        return redirect(url_for("home"))
    else:
        return '''
       <form action = "" method = "post">
          <p><input type ="text"      placeholder="Username" name = "username" required></p>
          <p><input type = "password" placeholder="password" name = "password" required></p>
          <p><input type ="submit" value ="登入"/></p>
       </form>
               '''

@app.route('/logout')
def logout():
    session.pop('username'  , None)
    session.pop('password'  , None)
    return redirect(url_for('home'))

if __name__ == "__main__" :
    webbrowser.open('http://127.0.0.1:5000/home')
    app.run(debug=False)
