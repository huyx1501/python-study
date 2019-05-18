#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pymysql

conn = pymysql.connect(host="192.168.2.114", port=3306, user="root", password="12345678", db="python_test")
cursor = conn.cursor()

cursor.execute("SELECT * FROM `person`;")
print(cursor.fetchone())  # 获取第1行数据
print(cursor.fetchone())  # 再获取1行数据
print(cursor.fetchmany(2))  # 接着获取2行数据
print(cursor.fetchall())  # 获取剩下的所有数据

cursor.close()
conn.close()
