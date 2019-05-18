#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 创建连接引擎
engine = create_engine("mysql+pymysql://root:12345678@192.168.2.114/python_test?charset=utf8")
BaseClass = declarative_base()  # 创建基类

# 书和作者映射表(直接创建对象而不是类，因为此表不需要手工插入数据，由ORM自动维护)
BookAuthors = Table(
    'book_authors',  # 表明
    BaseClass.metadata,  # metadata
    Column('book_id', Integer, ForeignKey("book.id")),
    Column('author_id', Integer, ForeignKey("author.id")),
)


# 创建表对象
class Author(BaseClass):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "email": self.email})


class Book(BaseClass):
    __tablename__ = "book"  # 表名
    id = Column(Integer, primary_key=True, )  # 主键
    name = Column(String(50))  # 列
    # 通过relationship
    authors = relationship(Author, secondary=BookAuthors, backref="books")

    def __repr__(self):
        return str({"id": self.id, "name": self.name})


# 创建表
BaseClass.metadata.create_all(engine)

# 创建会话（连接）类并实例化
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# b1 = Book(id=1, name="Python从入门到放弃")
# b2 = Book(id=2, name="Java从入门到放弃")
# b3 = Book(id=3, name="C++从入门到放弃")
#
# a1 = Author(id=1, name="张全蛋")
# a2 = Author(id=2, name="李二狗")
# a3 = Author(id=3, name="王尼玛")
#
# b1.authors = [a1, a2]
# b2.authors = [a1, a3]
# b3.authors = [a3]
#
# session.add_all([a1, a2, a3, b1, b2, b3])
# session.commit()

# print(session.query(Author).all())
# print(session.query(Book).all())
# print(session.query(BookAuthors).all())

author = session.query(Author).filter(Author.id == 1).first()
print(author.books)  # 查询作者参与的书
book = session.query(Book).filter(Book.id == 1).first()
print(book.authors)  # 查询书的作者
