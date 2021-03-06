#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import *
import os
import hashlib
import traceback
import datetime
import socketserver

# 创建连接引擎
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(
    mysql_config["User"],
    mysql_config["Password"],
    mysql_config["Host"],
    mysql_config["Port"],
    mysql_config["DBName"],
    mysql_config["Charset"]))

BaseClass = declarative_base()  # 创建基类
SessionClass = sessionmaker(bind=engine)


def get_md5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()
