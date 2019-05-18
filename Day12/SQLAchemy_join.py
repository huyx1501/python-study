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
class Student(BaseClass):
    __tablename__ = "student"  # 表名
    std_id = Column(Integer, primary_key=True)  # 主键
    name = Column(String(50))  # 列
    sex = Column(String(32))
    age = Column(SmallInteger)

    def __repr__(self):
        return str({"std_id": self.std_id, "name": self.name, "sex": self.sex, "age": self.age})


class Score(BaseClass):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("student.std_id"))  # 通过表的列名建立外键关联
    score = Column(SmallInteger, nullable=False, default=0)

    student = relationship(Student, backref="score")  # 建立关系，允许在student表中相关的外键查询对应的record记录

    def __repr__(self):
        return str({"id": self.id, "uid": self.uid, "score": self.score})


# 创建表
BaseClass.metadata.create_all(engine)

# 创建会话（连接）类并实例化
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

result = session.query(Student.name, Score.score).filter(Student.std_id == Score.uid).all()  # 手工联合字段查询
print(result)
join_result = session.query(Student.name, Score.score).join(Score).all()  # 自动根据外键关联联合查询
print(join_result)



