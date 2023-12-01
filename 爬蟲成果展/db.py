# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 11:18:22 2023

@author: willy
"""

'''________________pip install mysqlclient__'''
'''________________pip install flask_paginate__'''
# 安裝 mysqlclient，這是一個 Python 的 MySQL 庫

import MySQLdb


conn = MySQLdb.connect(host   = '127.0.0.1' ,   # 本地端IP 地址、localhost = 127.0.0.1 
                       user   = 'root' ,        # 使用者名稱，這裡使用最高權限的 root
                       passwd = '1234567890' ,  # MySQL 的密碼
                       db     = 'rong' ,        # 要連接的資料庫名稱
                       port   = 3306,           # MySQL 服務的埠號，預設是 3306
                       charset="utf8mb4")

cursor = conn.cursor()

"""資料庫"""

# mysql> create database rong default character set utf8mb4 collate utf8mb4_general_ci;
# Query OK, 1 row affected, 2 warnings (0.01 sec)

# mysql> use rong
# Database changed

# mysql> create table twfoods(
#     -> id int primary key auto_increment,
#     -> title varchar(100),
#     -> link_url varchar(300),
#     -> photo_url varchar(300),
#     -> ingredients varchar(300),
#     -> platform varchar(20));
# Query OK, 0 rows affected (0.02 sec)

# mysql> create table jpfoods(
#     -> id int primary key auto_increment,
#     -> title varchar(100),
#     -> link_url varchar(300),
#     -> photo_url varchar(300),
#     -> star float,
#     -> platform varchar(20));
# Query OK, 0 rows affected (0.09 sec)

# mysql> create table travel(
#     -> id int primary key auto_increment,
#     -> title varchar(100),
#     -> link_url varchar(300),
#     -> photo_url varchar(300),
#     -> price varchar(10),
#     -> date varchar(10),
#     -> platform varchar(20));
# Query OK, 0 rows affected (0.04 sec)

# mysql> create table Ifoods(
#     -> id int primary key auto_increment,
#     -> title varchar(100),
#     -> link_url varchar(300),
#     -> photo_url varchar(300),
#     -> address varchar(100),
#     -> platform varchar(20));
# Query OK, 0 rows affected (0.05 sec)

# mysql> create table contact(
#     -> id int primary key auto_increment,
#     -> subject varchar(50),
#     -> name varchar(50),
#     -> email varchar(50),
#     -> content text,
#     -> create_date date);
# Query OK, 0 rows affected (0.02 sec)















