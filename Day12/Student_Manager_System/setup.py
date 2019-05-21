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
    """
    学生表
    """
    __tablename__ = "%s_student" % mysql_config["Prefix"]  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    name = Column(String(64), nullable=False, comment="学生姓名", index=True)  # 列
    sex = Column(String(32), nullable=False, comment="性别")
    age = Column(SmallInteger, comment="年龄")
    join_time = Column(DateTime, comment="学生入学时间", index=True)
    status = Column(SmallInteger, nullable=False, default=1, comment="学生状态 0-毕业 1-在校")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "age": self.age, "join_time": self.join_time,
                    "status": "在校" if self.status == 1 else "毕业"})


class Teacher(BaseClass):
    """
    教师表
    """
    __tablename__ = "%s_teacher" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, comment="教师姓名", index=True)
    sex = Column(String(32), nullable=False, comment="性别")
    age = Column(SmallInteger, comment="年龄")
    join_time = Column(DateTime, nullable=False, comment="就职时间", index=True)
    status = Column(SmallInteger, nullable=False, default=1, comment="教师状态 0-离职 1-在职")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "age": self.age, "join_time": self.join_time,
                    "status": "在职" if self.status == 1 else "离职"})


class SysUser(BaseClass):
    """
    系统用户表
    """
    __tablename__ = "%s_sys_user" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, comment="管理员姓名")
    sex = Column(String(32), comment="性别")
    type = Column(Integer, nullable=False, default=1, comment="管理员类型 0-系统管理员， 1-普通管理员")
    create_time = Column(DateTime, comment="用户创建时间")
    update_time = Column(DateTime, comment="用户信息更新时间")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "type": self.type,
                    "create_time": self.create_time, "update_time": self.update_time})


class User(BaseClass):
    """
    账户表，用于登陆系统，包括学生账户、教师账户和系统账户（管理员）
    """
    __tablename__ = "%s_user" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, comment="登陆用户名", index=True)
    password = Column(String(255), nullable=False, comment="用户登陆密码")
    email = Column(String(255), comment="用户邮箱")
    phone = Column(String(64), comment="用户电话号码")
    create_time = Column(DateTime, comment="用户创建时间", index=True)
    update_time = Column(DateTime, comment="用户信息更新时间")
    role = Column(SmallInteger, nullable=False, comment="用户类型，0-管理员，1-学生，2-教师")
    member_id = Column(Integer,nullable=False, comment="绑定的学生或教师或系统用户ID")
    status = Column(SmallInteger, nullable=False, default=1, comment="用户状态，0-锁定，1-正常")

    def __repr__(self):
        return str({"id": self.id, "username": self.username, "password": "******", "email": self.email,
                    "phone": self.phone, "create_time": self.create_time, "update_time": self.update_time,
                    "role": self.role, "member_id": self.member_id, "status": "正常" if self.status == 1 else "锁定"})


class Province(BaseClass):
    """
    省级行政区
    """
    __tablename__ = "%s_province" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, comment="省（直辖市）")

    def __repr__(self):
        return str({"id": self.id, "name": self.name})


class City(BaseClass):
    """
    市级行政区
    """
    __tablename__ = "%s_city" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, comment="市（县）")

    def __repr__(self):
        return str({"id": self.id, "name": self.name})


class School(BaseClass):
    """
    学校表
    """
    __tablename__ = "%s_school" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment="学校名")
    create_time = Column(DateTime, comment="学校成立时间")
    address = Column(String(1024), comment="学校地址")
    province = Column(SmallInteger, comment="省代码")
    city = Column(SmallInteger, comment="市代码")
    status = Column(SmallInteger, nullable=False, default=1, comment="学校状态 0-关闭 1-开放")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "create_time": self.create_time, "address": self.address,
                    "province": self.province, "city": self.city, "status": "有效" if self.status == 1 else "无效"})


class Grade(BaseClass):
    """
    班级表
    """
    __tablename__ = "%s_grade" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment="班级名")
    course = Column(Integer, nullable=False, comment="课程ID")
    teacher = Column(Integer, nullable=False, comment="班主任ID")
    school = Column(Integer, nullable=False, comment="学校ID")
    create_time = Column(DateTime, nullable=False, comment="班级创建时间")
    status = Column(SmallInteger, nullable=False, default=1, comment="班级状态 0-关闭 1-开放")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "course": self.course, "teacher": self.teacher,
                    "create_time": self.create_time, "status": "开放" if self.status == 1 else "关闭"})


class Course(BaseClass):
    """
    课程表
    """
    __tablename__ = "%s_course" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment="课程名")
    create_time = Column(DateTime, comment="课程开设时间")
    status = Column(SmallInteger, nullable=False, default=1, comment="课程状态 0-无效 1-有效")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "create_time": self.create_time,
                    "status": "有效" if self.status == 1 else "无效"})


class Register(BaseClass):
    """
    学生注册记录
    """
    __tablename__ = "%s_register" % mysql_config["Prefix"]
    student_id = Column(Integer, primary_key=True, comment="学生ID")
    grade = Column(Integer, primary_key=True, comment="报名班级")
    register_time = Column(DateTime, comment="注册时间")
    register_cost = Column(Integer, comment="学费")

    def __repr__(self):
        return str({"student": self.student_id, "grade": self.grade, "register_time": self.register_time,
                    "cost": self.register_cost})


class TeacherJob(BaseClass):
    """
    教师任教记录
    """
    __tablename__ = "%s_teacher_job" % mysql_config["Prefix"]
    teacher_id = Column(Integer, primary_key=True, comment="教师ID")
    grade = Column(Integer, primary_key=True, comment="任教班级")
    begin_time = Column(DateTime, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    role = Column(SmallInteger, comment="任教类型 0-班主任 1-教师")

    def __repr__(self):
        return str({"student": self.teacher_id, "grade": self.grade, "begin_time": self.begin_time,
                    "end_time":self.end_time, "role": "教师" if self.role == 1 else "班主任"})


class Record(BaseClass):
    """
    上课记录
    """
    __tablename__ = "%s_record" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False, comment="学生ID", index=True)
    grade = Column(Integer, nullable=False, comment="班级ID", index=True)
    teacher = Column(Integer, nullable=False, comment="教师ID")
    class_sn = Column(Integer, nullable=False, comment="上课记录号（第几课）")
    status = Column(SmallInteger, nullable=False, default=1, comment="签到状态 0-未签到 1-已签到")
    create_time = Column(DateTime, nullable=False, comment="记录产生时间", index=True)

    def __repr__(self):
        return str({"id": self.id, "student": self.student_id, "grade": self.grade, "teacher": self.teacher,
                    "class_sn": self.class_sn, "status": "已签到" if self.status == 1 else "未签到",
                    "create_time": self.create_time})


class Score(BaseClass):
    """
    作业记录
    """
    __tablename__ = "%s_score" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False, comment="学生ID", index=True)
    grade = Column(Integer, nullable=False, comment="班级ID", index=True)
    create_time = Column(DateTime, comment="提交时间", index=True)
    score = Column(SmallInteger, comment="分数")
    score_time = Column(DateTime, comment="评分时间")
    teacher_id = Column(Integer, comment="评分教师")
    remark = Column(String(1024), comment="评语")

    def __repr__(self):
        return str({"id": self.id, "student": self.student_id, "grade": self.grade, "create_time": self.create_time,
                    "score": self.score, "score_time": self.score_time, "teacher": self.teacher_id,
                    "remark": self.remark})


if __name__ == "__main__":
    if os.path.isfile("install.lock"):
        exit("已初始化，如需重新初始化，请删除数据库表及install.lock文件后再次运行本程序")
    else:
        BaseClass.metadata.create_all(engine)
        with open("install.lock", "w", encoding="utf-8") as f:
            f.write("installed")
        print("系统初始化成功")

