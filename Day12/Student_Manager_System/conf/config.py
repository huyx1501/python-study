#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

"""
主配置文件，请按照注释修改mysql连接的相关信息
"""
# MySQL Connection
mysql_config = {
    "Host": "192.168.2.114",    # MySQL主机地址
    "Port": 3306,               # MySQL服务端口
    "User": "root",             # MySQL登陆用户名
    "Password": "12345678",     # MySQL登陆密码
    "DBName": "python_test",    # MySQL数据库名
    "Charset": "utf8"           # 数据库字符集
}
