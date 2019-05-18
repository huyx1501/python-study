#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pymysql

# 创建mysql连接
conn = pymysql.connect(host="192.168.2.114", port=3306, user="root", password="12345678", db="python_test")
cursor = conn.cursor()  # Create a new cursor to execute queries with.

# 创建数据表
cursor.execute('''
CREATE TABLE IF NOT EXISTS `person` (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NULL,
  `age` smallint(8) NULL,
  PRIMARY KEY (`id`));
  ''')

rows = cursor.execute("SELECT * FROM `person`;")  # 执行查询操作，返回匹配行数
print("Total rows: ", rows)

cursor.execute("INSERT INTO `person` (`name`, `age`) VALUES ('Tom', 22);")  # 插入
cursor.execute("INSERT INTO `person` (`name`, `age`) VALUES ('Jack', 23);")
rows = cursor.execute("SELECT * FROM `person`;")
print("Total rows: ", rows)

update_rows = cursor.execute("UPDATE `person` SET `age`=30 where `id`<%s;", 2)  # 传递参数到SQL语句
print("Updated rows: ", update_rows)
# 执行批量插入，传入一个由字段元组组成的列表
cursor.executemany("INSERT INTO `person` (`name`, `age`) VALUES (%s, %s);", [("Frank", 38), ("Mack", 27)])
rows = cursor.execute("SELECT * FROM `person`;")
print("Total rows: ", rows)

conn.commit()  # 提交操作（默认开启了事务，所有操作需要提交才能正式写入）
cursor.close()
conn.close()  # 关闭连接
