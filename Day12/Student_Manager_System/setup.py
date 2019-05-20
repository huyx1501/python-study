#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob
"""
用于初次使用时对数据库进行初始化，包括基本的表结构和测试数据。
初始化成功之后将在根目录下创建install.lock文件，表示已经初始化过，如需重新初始化，请手工删除所有表,
并删除install.lock文件后运行此脚本
"""
from conf import *
import os


class Student(BaseClass):
    __tablename__ = "sm_student"  # 表名
    id = Column(Integer, primary_key=True)  # 主键
    name = Column(String(50), comment="学生姓名")  # 列
    sex = Column(String(32), comment="性别")
    age = Column(SmallInteger, comment="年龄")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "age": self.age})


class Teacher(BaseClass):
    __tablename__ = "sm_teacher"  # 表名
    id = Column(Integer, primary_key=True)  # 主键
    name = Column(String(50), comment="教师姓名")  # 列
    sex = Column(String(32), comment="性别")
    age = Column(SmallInteger, comment="年龄")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "age": self.age})


class SysUser(BaseClass):
    __tablename__ = "sm_sys_user"  # 表名
    id = Column(Integer, primary_key=True)  # 主键
    name = Column(String(50), comment="管理员姓名")  # 列
    sex = Column(String(32), comment="性别")
    type = Column(Integer, comment="管理员类型 0 系统管理员， 1 普通管理员")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "type": self.type})


class User(BaseClass):
    __tablename__ = "sm_user"  # 表名
    id = Column(Integer, primary_key=True)  # 主键
    username = Column(String(50), comment="登陆用户名")  # 列
    password = Column(String(32), comment="用户登陆密码")
    status = Column(SmallInteger, comment="用户状态，0 锁定，1 正常")
    create_time = Column(DateTime, comment="用户创建时间")
    update_time = Column(DateTime, comment="用户信息更新时间")
    role = Column(SmallInteger, comment="用户类型，0 管理员，1 学生，2 教师")
    member_id = Column(Integer, comment="绑定的学生或教师或系统用户ID")

    def __repr__(self):
        return str({"id": self.id, "username": self.username, "password": self.password, "status": self.status,
                    "create_time": self.create_time, "update_time": self.update_time, "role": self.role,
                    "member_id": self.member_id})


if __name__ == "__main__":
    if os.path.isfile("install.lock"):
        exit("已初始化，如需重新初始化，请删除数据库表及install.lock文件后再次运行本程序")
    else:
        BaseClass.metadata.create_all(engine)
        with open("install.lock", "w", encoding="utf-8") as f:
            f.write("installed")
        print("系统初始化成功")

