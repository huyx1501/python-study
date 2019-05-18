#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from sqlalchemy import create_engine, Column, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建连接引擎
engine = create_engine("mysql+pymysql://root:12345678@192.168.2.114/python_test", encoding="utf-8", echo=False)
BaseClass = declarative_base()  # 创建基类


# 创建表对象
class Student(BaseClass):
    __tablename__ = "student"  # 表名
    std_id = Column(Integer, primary_key=True)  # 主键
    name = Column(String(50))  # 列
    sex = Column(String(32))
    age = Column(SmallInteger)


# 创建表
BaseClass.metadata.create_all(engine)

# 创建会话（连接）类并实例化
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

data1 = Student(name="Tommy", sex="M", age=28)  # 实例化要插入的数据
data2 = Student(name="Jack", sex="M", age=27)
session.add(data1)  # 准备插入
session.add(data2)
session.commit()  # 提交，正式插入
