#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .config import *

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
