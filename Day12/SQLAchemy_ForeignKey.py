#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 创建连接引擎
engine = create_engine("mysql+pymysql://root:12345678@192.168.2.114/python_test", encoding="utf-8", echo=False)
BaseClass = declarative_base()  # 创建基类


# 创建表对象
class Student(BaseClass):
    __tablename__ = "student"  # 表名
    std_id = Column(Integer, primary_key=True, )  # 主键
    name = Column(String(50))  # 列
    sex = Column(String(32))
    age = Column(SmallInteger)

    def __repr__(self):
        return str({"std_id": self.std_id, "name": self.name, "sex": self.sex, "age": self.age})


class Course(BaseClass):
    __tablename__ = "course"
    cid = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return str({"cid": self.cid, "name": self.name})


class Record(BaseClass):
    __tablename__ = "record"
    id = Column(Integer, primary_key=True)
    cid = Column(Integer, ForeignKey(Course.cid))  # 通过对象属性建立外键关联
    uid = Column(Integer, ForeignKey("student.std_id"))  # 通过表的列名建立外键关联
    score = Column(SmallInteger, nullable=False, default=0)
    # 建立关系，可通过外键关联查询到关系表中的相关记录，同时允许在对应的表中通过backref指定的字段查询本表中的对于记录
    student = relationship(Student, backref="record")
    course = relationship(Course, backref="record")

    def __repr__(self):
        return str({"student": self.student.name, "course": self.course.name, "score": self.score})


# 创建表
BaseClass.metadata.create_all(engine)

# 创建会话（连接）类并实例化
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

result = session.query(Student).filter(Student.std_id == 3).first()
for i in result.record:
    print(i)

# print(session.query(Student).all())
# print(session.query(Course).all())
# print(session.query(Record).all())
