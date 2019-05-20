#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob


from conf import *


class Student(BaseClass):
    __tablename__ = "student"  # 表名
    std_id = Column(Integer, primary_key=True)  # 主键
    name = Column(String(50))  # 列
    sex = Column(String(32))
    age = Column(SmallInteger)

    def __repr__(self):
        return str({"std_id": self.std_id, "name": self.name, "sex": self.sex, "age": self.age})


def main():
    # 创建会话（连接）类并实例化
    session = SessionClass()
    print(session.query(Student).all())


if __name__ == "__main__":
    main()
