#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 创建连接引擎
engine = create_engine("mysql+pymysql://root:12345678@192.168.2.114/python_test?charset=utf8")
BaseClass = declarative_base()  # 创建基类


# 创建表对象
class City(BaseClass):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return str({"id": self.id, "name": self.name})


class Student(BaseClass):
    __tablename__ = "student"  # 表名
    std_id = Column(Integer, primary_key=True, )  # 主键
    name = Column(String(50))  # 列
    sex = Column(String(32))
    age = Column(SmallInteger)
    home_address_code = Column(Integer, ForeignKey(City.id))  # 建立外键关联
    living_address_code = Column(Integer, ForeignKey(City.id))

    home_address = relationship(City, foreign_keys=[home_address_code])  # 指定foreign_keys建立联系
    # 不能在同一个表的多个外键关联中使用同一个backref名称
    living_address = relationship(City, backref="student", foreign_keys=[living_address_code])

    def __repr__(self):
        return str({"std_id": self.std_id, "name": self.name, "sex": self.sex, "age": self.age,
                    "home_address": self.home_address, "living_address": self.living_address})


# 创建表
BaseClass.metadata.create_all(engine)

# 创建会话（连接）类并实例化
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

result = session.query(Student).filter(Student.std_id == 3).first()
print(result)

# print(session.query(Student).all())
# print(session.query(City).all())
