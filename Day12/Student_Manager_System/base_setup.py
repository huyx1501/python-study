#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob
"""
用于初次使用时对数据库进行初始化，包括基本的表结构和测试数据。
初始化成功之后将在根目录下创建install.lock文件，表示已经初始化过，如需重新初始化，请手工删除所有表,
并删除install.lock文件后运行此脚本
"""
from conf import *


class UserInfo(BaseClass):
    """
    用户信息表
    """
    __tablename__ = "%s_user_info" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, comment="用户姓名", index=True)
    sex = Column(String(32), nullable=False, comment="性别 M-男性 F-女性")
    age = Column(SmallInteger, comment="年龄")
    update_time = Column(DateTime, comment="资料更新时间")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "age": self.age,
                    "update_time": s_time(self.update_time)})


class User(BaseClass):
    """
    账户表，用于登陆系统，包括学生账户、教师账户和系统账户（管理员）
    """
    __tablename__ = "%s_user" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String(255), nullable=False, comment="登陆用户名", index=True, unique=True)
    password = Column(String(255), nullable=False, comment="用户登陆密码")
    email = Column(String(255), comment="用户邮箱")
    phone = Column(String(64), comment="用户电话号码")
    create_time = Column(DateTime, comment="用户创建时间", index=True)
    member_id = Column(Integer, nullable=False, comment="绑定的学生或教师或系统用户ID")
    group_id = Column(Integer, comment="用户所属组")
    status = Column(SmallInteger, nullable=False, default=1, comment="用户状态，0-锁定，1-正常")

    def __repr__(self):
        return str({"id": self.id, "username": self.username, "email": self.email,
                    "phone": self.phone, "create_time": s_time(self.create_time),
                    "member_id": self.member_id, "group_id": self.group_id,
                    "status": "正常" if self.status == 1 else "锁定"})


class UserGroup(BaseClass):
    """
    用户组
    """
    __tablename__ = "%s_user_group" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_type = Column(SmallInteger, nullable=False, comment="组类型 1-管理员 2-学校管理员 3-普通用户")
    group_name = Column(String(255), nullable=False, comment="组名")

    def __repr__(self):
        return str({"id": self.id, "group_type": self.group_type, "group_name": self.group_name})


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
        return str({"id": self.id, "name": self.name, "create_time": s_time(self.create_time), "address": self.address,
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
                    "create_time": s_time(self.create_time), "status": "开放" if self.status == 1 else "关闭"})


class Course(BaseClass):
    """
    课程表
    """
    __tablename__ = "%s_course" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment="课程名")
    status = Column(SmallInteger, nullable=False, default=1, comment="课程状态 0-无效 1-有效")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "status": "有效" if self.status == 1 else "无效"})


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
        return str({"student": self.student_id, "grade": self.grade, "register_time": s_time(self.register_time),
                    "cost": self.register_cost})


class Record(BaseClass):
    """
    上课记录
    """
    __tablename__ = "%s_record" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False, comment="学生ID", index=True)
    grade = Column(Integer, nullable=False, comment="班级ID", index=True)
    teacher_id = Column(Integer, nullable=False, comment="教师ID")
    class_sn = Column(Integer, nullable=False, comment="上课记录号（第几课）")
    status = Column(SmallInteger, nullable=False, default=1, comment="签到状态 0-未签到 1-已签到")
    create_time = Column(DateTime, nullable=False, comment="记录产生时间", index=True)

    def __repr__(self):
        return str({"id": self.id, "student": self.student_id, "grade": self.grade, "teacher": self.teacher_id,
                    "class_sn": self.class_sn, "status": "已签到" if self.status == 1 else "未签到",
                    "create_time": s_time(self.create_time)})


class Score(BaseClass):
    """
    作业记录
    """
    __tablename__ = "%s_score" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False, comment="学生ID", index=True)
    record_id = Column(Integer, nullable=False, comment="对应的上课记录", index=True)
    create_time = Column(DateTime, comment="提交时间", index=True)
    score = Column(SmallInteger, comment="分数", index=True)
    rating_time = Column(DateTime, comment="评分时间")
    teacher_id = Column(Integer, comment="评分教师")
    remark = Column(String(1024), comment="评语")

    def __repr__(self):
        return str({"id": self.id, "student": self.student_id, "grade": self.record_id,
                    "create_time": s_time(self.create_time), "score": self.score,
                    "score_time": s_time(self.rating_time), "teacher": self.teacher_id, "remark": self.remark})


class Menu(BaseClass):
    """
    菜单项
    """
    __tablename__ = "%s_menu" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment="父菜单ID")
    code = Column(String(50), comment="菜单对应的处理方法", index=True)
    name = Column(String(50), nullable=False, comment="菜单名称")
    status = Column(SmallInteger, nullable=False, default=1, comment="菜单状态 0-关闭 1-开放")

    def __repr__(self):
        return str({"id": self.id, "pid": self.pid, "code": self.code, "name": self.name,
                    "status": "有效" if self.status == 1 else "无效"})


class UserRole(BaseClass):
    """
    菜单权限
    """
    __tablename__ = "%s_user_role" % mysql_config["Prefix"]
    menu_id = Column(Integer, nullable=False, comment="菜单ID", primary_key=True)
    user_id = Column(Integer, nullable=True, comment="用户ID", primary_key=True)
    role_type = Column(SmallInteger, nullable=False, default=1, comment="权限（暂未启用） 1-只读 2-新增 3-修改 4-全部")

    def __repr__(self):
        return str({"menu_id": self.menu_id, "user_id": self.user_id, "role_type": self.role_type})


class GroupRole(BaseClass):
    """
    菜单权限
    """
    __tablename__ = "%s_group_role" % mysql_config["Prefix"]
    menu_id = Column(Integer, nullable=False, comment="菜单ID", primary_key=True)
    group_id = Column(Integer, nullable=True, comment="用户组ID", primary_key=True)
    role_type = Column(SmallInteger, nullable=False, default=1, comment="权限（暂未启用） 1-只读 2-新增 3-修改 4-全部")

    def __repr__(self):
        return str({"menu_id": self.menu_id, "user_id": self.group_id, "role_type": self.role_type})


def s_time(time):
    if time:
        return time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return ""


def initialize():
    """
    初始化数据
    """
    session = SessionClass()
    # 地址
    a1 = Province(id=1, name="北京")
    a2 = Province(id=2, name="上海")
    a3 = Province(id=3, name="广东")
    c1 = City(id=1, name="北京市")
    c2 = City(id=2, name="上海市")
    c3 = City(id=3, name="广州")
    c4 = City(id=4, name="深圳")
    session.add_all([a1, a2, a3, c1, c2, c3, c4])

    # 课程
    cou1 = Course(id=1, name="Python")
    cou2 = Course(id=2, name="PHP")
    cou3 = Course(id=3, name="Java")
    session.add_all([cou1, cou2, cou3])

    # 学校
    s1 = School(id=1, name="武当派", create_time=datetime.datetime.strptime("2011-05-05", "%Y-%m-%d"), address="武当山",
                province=2, city=2)
    s2 = School(id=2, name="少林派", create_time=datetime.datetime.strptime("2010-06-12", "%Y-%m-%d"), address="嵩山",
                province=1, city=1)
    session.add_all([s1, s2])

    # 班级
    g1 = Grade(id=1, name="Python全栈第8期", course=1, teacher=3, school=2,
               create_time=datetime.datetime.strptime("2017-09-21", "%Y-%m-%d"), status=0)
    g2 = Grade(id=2, name="Java从入门到放弃", course=3, teacher=2, school=1,
               create_time=datetime.datetime.strptime("2018-08-20", "%Y-%m-%d"))
    g3 = Grade(id=3, name="Python自动化第3期", course=1, teacher=3, school=1,
               create_time=datetime.datetime.strptime("2018-12-25", "%Y-%m-%d"))
    session.add_all([g1, g2, g3])

    # 用户组
    ug1 = UserGroup(id=1, group_type=1, group_name="系统管理员")
    ug2 = UserGroup(id=2, group_type=2, group_name="学校管理员")
    ug3 = UserGroup(id=3, group_type=3, group_name="教师")
    ug4 = UserGroup(id=4, group_type=4, group_name="学生")
    session.add_all([ug1, ug2, ug3, ug4])

    # 教师
    t1 = UserInfo(id=100, name="张三丰", sex="M", age=65)
    t2 = UserInfo(id=101, name="王重阳", sex="M", age=60)
    t3 = UserInfo(id=102, name="紫霞仙子", sex="F", age=200)
    # 学生
    st1 = UserInfo(id=1001, name="张无忌", sex="M", age=18)
    st2 = UserInfo(id=1002, name="黄蓉", sex="F", age=22)
    st3 = UserInfo(id=1003, name="段誉", sex="M", age=19)
    # 管理员
    su1 = UserInfo(id=1, name="伊利丹.怒风", sex="M", age=30)
    session.add_all([t1, t2, t3, st1, st2, st3, su1])

    # 用户表
    u1 = User(id=1, username="Admin", password=get_md5("12345678"), create_time=datetime.datetime.now(), group_id=1,
              member_id=1)
    u2 = User(id=2, username="ZhangSF", password=get_md5("123123"),
              create_time=datetime.datetime.strptime("2011-04-12", "%Y-%m-%d"), group_id=2, member_id=1)
    u3 = User(id=3, username="WangCY", password=get_md5("123123"),
              create_time=datetime.datetime.strptime("2012-06-19", "%Y-%m-%d"), group_id=3, member_id=2)
    u4 = User(id=4, username="ZiXia", password=get_md5("123123"),
              create_time=datetime.datetime.strptime("2015-03-24", "%Y-%m-%d"), group_id=3, member_id=3)
    u5 = User(id=5, username="ZhangWJ", password=get_md5("456456"),
              create_time=datetime.datetime.strptime("2017-04-12", "%Y-%m-%d"), group_id=4, member_id=1)
    u6 = User(id=6, username="HuangR", password=get_md5("456456"),
              create_time=datetime.datetime.strptime("2017-05-13", "%Y-%m-%d"), group_id=4, member_id=2)
    u7 = User(id=7, username="DuanY", password=get_md5("456456"),
              create_time=datetime.datetime.strptime("2018-01-22", "%Y-%m-%d"), group_id=4, member_id=3)
    session.add_all([u1, u2, u3, u4, u5, u6, u7])

    # 菜单表
    session.add_all([
        # 一级菜单
        Menu(id=1, name="个人中心"),
        Menu(id=2, name="学习中心"),
        Menu(id=3, name="教务中心"),
        Menu(id=4, name="系统管理"),

        # 二级菜单
        Menu(id=101, pid=1, code="info_mod", name="资料修改"),
        Menu(id=102, pid=1, code="change_pass", name="密码修改"),

        Menu(id=103, pid=2, code="sign_in", name="上课签到"),
        Menu(id=104, pid=2, code="submit", name="提交作业"),
        Menu(id=105, pid=2, code="query_score", name="成绩查询"),
        Menu(id=106, pid=2, code="sign_up", name="报名新课程"),

        Menu(id=107, pid=3, name="班级管理"),
        Menu(id=108, pid=3, name="教师管理"),
        Menu(id=109, pid=3, name="上课管理"),
        Menu(id=110, pid=3, name="作业管理"),

        Menu(id=111, pid=4, name="用户管理"),
        Menu(id=112, pid=4, name="课程管理"),
        Menu(id=113, pid=4, name="学校管理"),
        Menu(id=114, pid=4, name="地址管理"),
        Menu(id=115, pid=4, name="权限管理"),

        # 三级级菜单
        Menu(id=1001, pid=107, code="class_query", name="查询班级"),
        Menu(id=1002, pid=107, code="class_add", name="添加班级"),
        Menu(id=1003, pid=107, code="class_mod", name="修改班级"),
        Menu(id=1004, pid=107, code="class_del", name="删除班级"),

        Menu(id=1005, pid=108, code="teacher_query", name="查询教师信息"),
        Menu(id=1006, pid=108, code="teacher_add", name="聘用教师"),
        Menu(id=1007, pid=108, code="teacher_mod", name="修改教师信息"),
        Menu(id=1008, pid=108, code="teacher_del", name="解聘教师"),

        Menu(id=1009, pid=109, code="record_query", name="查询上课记录"),
        Menu(id=1010, pid=109, code="record_add", name="添加上课记录"),
        Menu(id=1011, pid=109, code="record_del", name="查询上课记录"),

        Menu(id=1012, pid=110, code="work_query", name="查询作业信息"),
        Menu(id=1013, pid=110, code="work_add", name="布置作业"),
        Menu(id=1014, pid=110, code="work_score", name="批改作业"),
        Menu(id=1015, pid=110, code="work_del", name="删除作业"),

        Menu(id=1016, pid=111, code="user_query", name="查询用户"),
        Menu(id=1017, pid=111, code="user_add", name="添加用户"),
        Menu(id=1018, pid=111, code="user_mod", name="修改用户"),
        Menu(id=1019, pid=111, code="user_del", name="删除用户"),

        Menu(id=1020, pid=112, code="course_query", name="查询课程"),
        Menu(id=1021, pid=112, code="course_add", name="添加课程"),
        Menu(id=1022, pid=112, code="course_mod", name="修改课程"),
        Menu(id=1023, pid=112, code="course_del", name="删除课程"),

        Menu(id=1024, pid=113, code="school_query", name="查询学校"),
        Menu(id=1025, pid=113, code="school_add", name="添加学校"),
        Menu(id=1026, pid=113, code="school_mod", name="修改学校"),
        Menu(id=1027, pid=113, code="school_del", name="删除学校"),

        Menu(id=1028, pid=114, name="省份管理"),
        Menu(id=1029, pid=114, name="城市管理"),

        Menu(id=1030, pid=115, code="auth_query", name="查询权限"),
        Menu(id=1031, pid=115, code="auth_add", name="添加权限"),
        Menu(id=1032, pid=115, code="auth_mod", name="修改权限"),
        Menu(id=1033, pid=115, code="auth_del", name="删除权限"),

        # 四级菜单
        Menu(id=10001, pid=1013, code="prov_query", name="查询省份"),
        Menu(id=10002, pid=1013, code="prov_add", name="添加省份"),
        Menu(id=10003, pid=1013, code="prov_mod", name="修改省份"),
        Menu(id=10004, pid=1013, code="prov_del", name="删除省份"),
        Menu(id=10005, pid=1014, code="city_query", name="查询城市"),
        Menu(id=10006, pid=1014, code="city_add", name="添加城市"),
        Menu(id=10007, pid=1014, code="city_mod", name="修改城市"),
        Menu(id=10008, pid=1014, code="city_del", name="删除城市"),
    ])

    # 菜单权限表
    session.add_all([
        # 一级菜单
        GroupRole(menu_id=1, group_id=1),
        GroupRole(menu_id=1, group_id=2),
        GroupRole(menu_id=1, group_id=3),
        GroupRole(menu_id=1, group_id=4),
        GroupRole(menu_id=2, group_id=4),
        GroupRole(menu_id=3, group_id=1),
        GroupRole(menu_id=3, group_id=2),
        GroupRole(menu_id=4, group_id=1),
        # 二级菜单
        GroupRole(menu_id=101, group_id=1),
        GroupRole(menu_id=101, group_id=2),
        GroupRole(menu_id=101, group_id=3),
        GroupRole(menu_id=101, group_id=4),
        GroupRole(menu_id=102, group_id=1),
        GroupRole(menu_id=102, group_id=2),
        GroupRole(menu_id=102, group_id=3),
        GroupRole(menu_id=102, group_id=4),

        GroupRole(menu_id=103, group_id=4),
        GroupRole(menu_id=104, group_id=4),
        GroupRole(menu_id=105, group_id=4),
        GroupRole(menu_id=106, group_id=4),

        GroupRole(menu_id=107, group_id=1),
        GroupRole(menu_id=108, group_id=1),
        GroupRole(menu_id=107, group_id=2),
        GroupRole(menu_id=108, group_id=2),
        GroupRole(menu_id=109, group_id=2),
        GroupRole(menu_id=110, group_id=2),
        GroupRole(menu_id=109, group_id=3),
        GroupRole(menu_id=110, group_id=3),

        GroupRole(menu_id=112, group_id=1),
        GroupRole(menu_id=113, group_id=1),
        GroupRole(menu_id=114, group_id=1),
        GroupRole(menu_id=115, group_id=1),

        # 三级菜单
        # 系统管理员
        GroupRole(menu_id=1016, group_id=1),
        GroupRole(menu_id=1017, group_id=1),
        GroupRole(menu_id=1018, group_id=1),
        GroupRole(menu_id=1019, group_id=1),
        GroupRole(menu_id=1020, group_id=1),
        GroupRole(menu_id=1021, group_id=1),
        GroupRole(menu_id=1022, group_id=1),
        GroupRole(menu_id=1023, group_id=1),
        GroupRole(menu_id=1024, group_id=1),
        GroupRole(menu_id=1025, group_id=1),
        GroupRole(menu_id=1026, group_id=1),
        GroupRole(menu_id=1027, group_id=1),
        GroupRole(menu_id=1028, group_id=1),
        GroupRole(menu_id=1029, group_id=1),
        GroupRole(menu_id=1030, group_id=1),
        GroupRole(menu_id=1031, group_id=1),
        GroupRole(menu_id=1032, group_id=1),
        GroupRole(menu_id=1033, group_id=1),
        # 学校管理员
        GroupRole(menu_id=1001, group_id=2),
        GroupRole(menu_id=1002, group_id=2),
        GroupRole(menu_id=1003, group_id=2),
        GroupRole(menu_id=1004, group_id=2),
        GroupRole(menu_id=1005, group_id=2),
        GroupRole(menu_id=1006, group_id=2),
        GroupRole(menu_id=1007, group_id=2),
        GroupRole(menu_id=1008, group_id=2),
        GroupRole(menu_id=1009, group_id=2),
        GroupRole(menu_id=1010, group_id=2),
        GroupRole(menu_id=1011, group_id=2),
        # 教师
        GroupRole(menu_id=1009, group_id=3),
        GroupRole(menu_id=1010, group_id=3),
        GroupRole(menu_id=1011, group_id=3),
        GroupRole(menu_id=1012, group_id=3),
        GroupRole(menu_id=1013, group_id=3),
        GroupRole(menu_id=1014, group_id=3),
        GroupRole(menu_id=1015, group_id=3),

        # 四级菜单
        GroupRole(menu_id=10001, group_id=1),
        GroupRole(menu_id=10002, group_id=1),
        GroupRole(menu_id=10003, group_id=1),
        GroupRole(menu_id=10004, group_id=1),
        GroupRole(menu_id=10005, group_id=1),
        GroupRole(menu_id=10006, group_id=1),
        GroupRole(menu_id=10007, group_id=1),
        GroupRole(menu_id=10008, group_id=1),

        UserRole(menu_id=3, user_id=1),
        UserRole(menu_id=109, user_id=1),
        UserRole(menu_id=110, user_id=1),
        UserRole(menu_id=111, user_id=1),
        UserRole(menu_id=1009, user_id=1),
        UserRole(menu_id=1012, user_id=1),
    ])

    session.commit()  # 插入数据


if __name__ == "__main__":
    if os.path.isfile("install.lock"):
        exit("已初始化，如需重新初始化，请删除数据库表及install.lock文件后再次运行本程序")
    else:
        BaseClass.metadata.create_all(engine)
        initialize()
        with open("install.lock", "w", encoding="utf-8") as f:
            f.write("installed")
        print("系统初始化成功")
