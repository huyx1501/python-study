import db_handler


class Schools(object):
    """
    学校类
    """
    def __init__(self, name, addr):
        self.name = name  # 学校名
        self.addr = addr  # 学校地址
        self.teachers = []  # 学校所有的老师
        self.students = []  # 学校所有的学生
        self.classes = []  # 学校所有的班级

    def registry(self, student, cls):
        self.students.append(student)  # 将学生添加到本校学生列表
        student.school.append(self)  # 将本校添加到学生已报名的学校列表
        student.classes.append(cls)  # 将本班级添加到学生已报名的班级列表
        cls.student.append(student)  # 将学生添加到班级的学生列表
        print("[%s]注册成为[%s][%s%s]班学生成功" % (student.name, self.name, cls.teacher.name, cls.course.name))

    def hire(self, teacher, salary):
        print("欢迎[%s]老师加入[%s]" % (teacher.name, self.name))
        self.teachers.append(teacher)  # 将老师添加到本校教师列表
        new_class = Classes(teacher.course.name, self, teacher.course, teacher)  # 根据教师所教的课程生成一个新的班级
        self.classes.append(new_class)  # 将新班级加入本校班级列表
        teacher.school = self  # 将本校设为老师所属的学校
        teacher.classes = new_class  # 将当前班级设为老师所属的班级
        teacher.salary = salary


class Classes(object):
    """
    班级类
    """
    def __init__(self, name, school, course, teacher):
        self.name = name  # 班级名
        self.school = school  # 班级所属学校
        self.course = course  # 班级所教的课程
        self.teacher = teacher  # 班级老师
        self.student = []  # 班级学生列表
        self.status = 0  # 班级上课状态，0未下课，1为上课中


class Courses(object):
    """
    课程类
    """
    def __init__(self, name, price, period):
        self.name = name  # 课程名
        self.price = price  # 课程价格
        self.period = period  # 课程周期（课时）


class Students(object):
    """
    学生类
    """
    def __init__(self, name, age, sex):
        self.name = name  # 学生姓名
        self.age = age  # 年龄
        self.sex = sex  # 性别
        self.school = []  # 学生已报名的学校列表
        self.classes = []  # 学生已报名的班级列表
        self.score = {}  # 学生在各班级的分数


class Teachers(object):
    """
    教师类
    """
    def __init__(self, name, age, sex, course):
        self.name = name  # 教师姓名
        self.age = age  # 年龄
        self.sex = sex  # 性别
        self.course = course  # 所教课程
        self.school = None  # 所属学校，默认空
        self.classes = None  # 所属班级，默认空
        self.salary = 0  # 薪资，默认无

    def start_class(self):
        if self.classes.status == 0:
            self.classes.status = 1
            print("上课啦")
        else:
            print("已经在上课了")

    def finish_class(self):
        if self.classes.status == 1:
            self.classes.status = 0
            print("下课啦")
        else:
            print("还未开始上课")


# 从存储的文件载入以前的对象信息
school_list = db_handler.load_info("school_list")
teacher_list = db_handler.load_info("teacher_list")
student_list = db_handler.load_info("student_list")
course_list = db_handler.load_info("course_list")
