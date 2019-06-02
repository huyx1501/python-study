#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob
"""
用于初次使用时对数据库进行初始化，包括基本的表结构和测试数据。
初始化成功之后将在根目录下创建install.lock文件，表示已经初始化过，如需重新初始化，请手工删除所有表,
并删除install.lock文件后运行此脚本
"""
from conf import *


class Student(BaseClass):
    """
    学生表
    """
    __tablename__ = "%s_student" % mysql_config["Prefix"]  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    name = Column(String(64), nullable=False, comment="学生姓名", index=True)  # 列
    sex = Column(String(32), nullable=False, comment="性别 M-男性 F-女性")
    age = Column(SmallInteger, comment="年龄")
    join_time = Column(DateTime, comment="学生入学时间", index=True)
    status = Column(SmallInteger, nullable=False, default=0, comment="学生状态 0-游离 1-在校 2-毕业")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "age": self.age,
                    "join_time": s_time(self.join_time), "status": self.status})


class Teacher(BaseClass):
    """
    教师表
    """
    __tablename__ = "%s_teacher" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, comment="教师姓名", index=True)
    sex = Column(String(32), nullable=False, comment="性别 M-男性 F-女性")
    age = Column(SmallInteger, comment="年龄")
    join_time = Column(DateTime, comment="就职时间", index=True)
    status = Column(SmallInteger, nullable=False, default=1, comment="教师状态 0-在野 1-在职")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "age": self.age,
                    "join_time": s_time(self.join_time), "status": self.status})


class SysUser(BaseClass):
    """
    系统用户表
    """
    __tablename__ = "%s_sys_user" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, comment="管理员姓名")
    sex = Column(String(32), comment="性别")
    u_type = Column(Integer, nullable=False, default=2, comment="管理员类型 1-系统管理员， 2-普通管理员")
    create_time = Column(DateTime, comment="用户创建时间")
    update_time = Column(DateTime, comment="用户信息更新时间")

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "sex": self.sex, "u_type": self.u_type,
                    "create_time": s_time(self.create_time), "update_time": s_time(self.update_time)})


class User(BaseClass):
    """
    账户表，用于登陆系统，包括学生账户、教师账户和系统账户（管理员）
    """
    __tablename__ = "%s_user" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, comment="登陆用户名", index=True, unique=True)
    password = Column(String(255), nullable=False, comment="用户登陆密码")
    email = Column(String(255), comment="用户邮箱")
    phone = Column(String(64), comment="用户电话号码")
    create_time = Column(DateTime, comment="用户创建时间", index=True)
    update_time = Column(DateTime, comment="用户信息更新时间")
    role = Column(SmallInteger, nullable=False, comment="用户类型，1-管理员，2-教师，3-学生")
    member_id = Column(Integer, nullable=False, comment="绑定的学生或教师或系统用户ID")
    status = Column(SmallInteger, nullable=False, default=1, comment="用户状态，0-锁定，1-正常")

    def __repr__(self):
        return str({"id": self.id, "username": self.username, "email": self.email,
                    "phone": self.phone, "create_time": s_time(self.create_time),
                    "update_time": s_time(self.update_time), "role": self.role, "member_id": self.member_id,
                    "status": "正常" if self.status == 1 else "锁定"})


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


class TeacherJob(BaseClass):
    """
    教师任教记录
    """
    __tablename__ = "%s_teacher_job" % mysql_config["Prefix"]
    teacher_id = Column(Integer, primary_key=True, comment="教师ID")
    grade = Column(Integer, primary_key=True, comment="任教班级")
    begin_time = Column(DateTime, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    role = Column(SmallInteger, comment="任教类型 1-班主任 2-教师")

    def __repr__(self):
        return str({"student": self.teacher_id, "grade": self.grade, "begin_time": s_time(self.begin_time),
                    "end_time": s_time(self.end_time), "role": "教师" if self.role == 1 else "班主任"})


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
    score_status = Column(Sm)
    create_time = Column(DateTime, nullable=False, comment="记录产生时间", index=True)

    def __repr__(self):
        return str({"id": self.id, "student": self.student_id, "grade": self.grade, "teacher": self.teacher,
                    "class_sn": self.class_sn, "status": "已签到" if self.status == 1 else "未签到",
                    "create_time": s_time(self.create_time)})


class Score(BaseClass):
    """
    作业记录
    """
    __tablename__ = "%s_score" % mysql_config["Prefix"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False, comment="学生ID", index=True)
    record_id = Column(Integer, ForeignKey(Record.id), nullable=False, comment="对应的上课记录", index=True)
    create_time = Column(DateTime, comment="提交时间", index=True)
    score = Column(SmallInteger, comment="分数")
    score_time = Column(DateTime, comment="评分时间")
    teacher_id = Column(Integer, ForeignKey(Teacher.id), comment="评分教师")
    remark = Column(String(1024), comment="评语")
    # 建立与其他表的关系，方便查找
    students = relationship(Student, backref="score")
    teachers = relationship(Teacher, backref="score")
    record = relationship(Record, backref="score")

    def __repr__(self):
        return str({"id": self.id, "student": self.student_id, "grade": self.record_id,
                    "create_time": s_time(self.create_time), "score": self.score, "score_time": s_time(self.score_time),
                    "teacher": self.teacher_id, "remark": self.remark})


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


class MenuRole(BaseClass):
    """
    菜单权限
    """
    __tablename__ = "%s_menu_role" % mysql_config["Prefix"]
    menu_id = Column(Integer, nullable=False, comment="菜单ID", primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID", primary_key=True)
    role_type = Column(SmallInteger, nullable=False, default=1, comment="权限 1-只读 2-新增 3-修改 4-全部")
    user = relationship(User, backref="menu_role")

    def __repr__(self):
        return str({"menu_id": self.menu_id, "user_id": self.user_id, "role_type": self.role_type})


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

    # 教师
    t1 = Teacher(id=1, name="张三丰", sex="M", age=65, status=0)
    t2 = Teacher(id=2, name="王重阳", sex="M", age=60, status=0)
    t3 = Teacher(id=3, name="紫霞仙子", sex="F", age=200, status=0)
    session.add_all([t1, t2, t3])

    # 学生
    st1 = Student(id=1, name="张无忌", sex="M", age=18, status=0)
    st2 = Student(id=2, name="黄蓉", sex="F", age=22, status=0)
    st3 = Student(id=3, name="段誉", sex="M", age=19, status=0)
    session.add_all([st1, st2, st3])

    # 系统用户表
    su1 = SysUser(id=1, name="伊利丹.怒风", sex="M", u_type=1, create_time=datetime.datetime.now())
    session.add_all([su1, ])

    # 用户表
    u1 = User(id=1, username="Admin", password=get_md5("12345678"), create_time=datetime.datetime.now(), role=1,
              member_id=1)
    u2 = User(id=2, username="ZhangSF", password=get_md5("123123"),
              create_time=datetime.datetime.strptime("2011-04-12", "%Y-%m-%d"), role=2, member_id=1)
    u3 = User(id=3, username="WangCY", password=get_md5("123123"),
              create_time=datetime.datetime.strptime("2012-06-19", "%Y-%m-%d"), role=2, member_id=2)
    u4 = User(id=4, username="ZiXia", password=get_md5("123123"),
              create_time=datetime.datetime.strptime("2015-03-24", "%Y-%m-%d"), role=2, member_id=3)
    u5 = User(id=5, username="ZhangWJ", password=get_md5("456456"),
              create_time=datetime.datetime.strptime("2017-04-12", "%Y-%m-%d"), role=3, member_id=1)
    u6 = User(id=6, username="HuangR", password=get_md5("456456"),
              create_time=datetime.datetime.strptime("2017-05-13", "%Y-%m-%d"), role=3, member_id=2)
    u7 = User(id=7, username="DuanY", password=get_md5("456456"),
              create_time=datetime.datetime.strptime("2018-01-22", "%Y-%m-%d"), role=3, member_id=3)
    session.add_all([u1, u2, u3, u4, u5, u6, u7])

    # 菜单表
    # 一级菜单
    session.add_all([
        Menu(id=1, name="用户管理"),
        Menu(id=2, name="地址管理"),
        Menu(id=3, name="课程管理"),
        Menu(id=4, name="学校管理"),
        Menu(id=5, name="菜单管理"),
        Menu(id=6, name="权限管理"),
        # 二级菜单
        Menu(id=7, pid=1, code="user_query", name="查询用户"),
        Menu(id=8, pid=1, code="user_add", name="添加用户"),
        Menu(id=9, pid=1, code="user_mod", name="修改用户"),
        Menu(id=10, pid=1, code="user_del", name="删除用户"),
        Menu(id=11, pid=2, name="省份管理"),
        Menu(id=12, pid=2, name="城市管理"),
        Menu(id=13, pid=3, code="course_query", name="查询课程"),
        Menu(id=14, pid=3, code="course_add", name="添加课程"),
        Menu(id=15, pid=3, code="course_mod", name="修改课程"),
        Menu(id=16, pid=3, code="course_del", name="删除课程"),
        Menu(id=17, pid=4, code="school_query", name="查询学校"),
        Menu(id=18, pid=4, code="school_add", name="添加学校"),
        Menu(id=19, pid=4, code="school_mod", name="修改学校"),
        Menu(id=20, pid=4, code="school_del", name="删除学校"),
        Menu(id=21, pid=5, code="menu_query", name="查询菜单"),
        Menu(id=22, pid=5, code="menu_mod", name="修改菜单"),
        Menu(id=23, pid=5, code="menu_add", name="添加菜单"),
        Menu(id=24, pid=5, code="menu_del", name="删除菜单"),
        Menu(id=25, pid=6, code="auth_query", name="查询权限"),
        Menu(id=26, pid=6, code="auth_add", name="添加权限"),
        Menu(id=27, pid=6, code="auth_mod", name="修改权限"),
        Menu(id=28, pid=6, code="auth_del", name="删除权限"),
        # 三级菜单
        Menu(id=29, pid=11, code="prov_query", name="查询省份"),
        Menu(id=30, pid=11, code="prov_add", name="添加省份"),
        Menu(id=31, pid=11, code="prov_mod", name="修改省份"),
        Menu(id=32, pid=11, code="prov_del", name="删除省份"),
        Menu(id=33, pid=12, code="city_query", name="查询城市"),
        Menu(id=34, pid=12, code="city_add", name="添加城市"),
        Menu(id=35, pid=12, code="city_mod", name="修改城市"),
        Menu(id=36, pid=12, code="city_del", name="删除城市"),
    ])

    # 菜单权限表
    session.add_all([
        MenuRole(menu_id=1, user_id=1, role_type=4),
        MenuRole(menu_id=2, user_id=1, role_type=4),
        MenuRole(menu_id=3, user_id=1, role_type=4),
        MenuRole(menu_id=4, user_id=1, role_type=4),
        MenuRole(menu_id=5, user_id=1, role_type=4),
        MenuRole(menu_id=6, user_id=1, role_type=4),
        MenuRole(menu_id=7, user_id=1, role_type=4),
        MenuRole(menu_id=8, user_id=1, role_type=4),
        MenuRole(menu_id=9, user_id=1, role_type=4),
        MenuRole(menu_id=10, user_id=1, role_type=4),
        MenuRole(menu_id=11, user_id=1, role_type=4),
        MenuRole(menu_id=12, user_id=1, role_type=4),
        MenuRole(menu_id=13, user_id=1, role_type=4),
        MenuRole(menu_id=14, user_id=1, role_type=4),
        MenuRole(menu_id=15, user_id=1, role_type=4),
        MenuRole(menu_id=16, user_id=1, role_type=4),
        MenuRole(menu_id=17, user_id=1, role_type=4),
        MenuRole(menu_id=18, user_id=1, role_type=4),
        MenuRole(menu_id=19, user_id=1, role_type=4),
        MenuRole(menu_id=20, user_id=1, role_type=4),
        MenuRole(menu_id=21, user_id=1, role_type=4),
        MenuRole(menu_id=22, user_id=1, role_type=4),
        MenuRole(menu_id=23, user_id=1, role_type=4),
        MenuRole(menu_id=24, user_id=1, role_type=4),
        MenuRole(menu_id=25, user_id=1, role_type=4),
        MenuRole(menu_id=26, user_id=1, role_type=4),
        MenuRole(menu_id=27, user_id=1, role_type=4),
        MenuRole(menu_id=28, user_id=1, role_type=4),
        MenuRole(menu_id=29, user_id=1, role_type=4),
        MenuRole(menu_id=30, user_id=1, role_type=4),
        MenuRole(menu_id=31, user_id=1, role_type=4),
        MenuRole(menu_id=32, user_id=1, role_type=4)
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
