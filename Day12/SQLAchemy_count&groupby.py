#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, func
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

    def __repr__(self):
        return str({"std_id": self.std_id, "name": self.name, "sex": self.sex, "age": self.age})


# 创建会话（连接）类并实例化
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# 相当于select student.sex, count(student.sex) from student group by student.sex
result = session.query(Student.sex, func.count(Student.sex)).group_by(Student.sex).all()
print(result)
