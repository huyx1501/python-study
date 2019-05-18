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

    def __repr__(self):
        return str({"std_id": self.std_id, "name": self.name, "sex": self.sex, "age": self.age})


# 创建会话（连接）类并实例化
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

select_result_all = session.query(Student).filter_by().all()  # 相当于select student.* from student，返回所有符合条件的类实例
print(select_result_all)  # select_result_all对象是Student的实例，通过重构对象的__repr__方法来获取自定义的信息

select_filtered1 = session.query(Student.name, Student.age).filter(Student.age > 20).all()  # 使用filter方法过滤
print(select_filtered1)

select_filtered2 = session.query(Student.name, Student.age).filter_by(std_id=2).all()  # 使用filter_by方法过滤
print(select_filtered2)

# 多条件查询
select_filtered3 = session.query(Student.name, Student.age).filter(Student.age > 20).filter(Student.std_id > 1).all()
print(select_filtered3)
