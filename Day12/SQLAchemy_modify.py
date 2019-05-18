#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from sqlalchemy import create_engine, Column, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建连接引擎
engine = create_engine("mysql+pymysql://root:12345678@192.168.2.114/python_test?charset=utf8")
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

select_student = session.query(Student).filter_by(std_id=2).first()  # 查询并返回第一条结果
print(select_student)
select_student.age = 20  # 修改对象属性
session.commit()  # 提交

new_student = Student(name="Lincoln", age=26)  # 创建新对象
session.add(new_student)  # 加入session
print(session.query(Student).filter(Student.name == "Lincoln").all())  # 查询结果
session.rollback()  # 回滚
print(session.query(Student).filter(Student.name == "Lincoln").all())  # 再次查询
