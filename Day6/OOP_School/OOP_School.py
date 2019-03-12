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


# 初始化课程
Java = Courses("Java", 15000, 60)
Go = Courses("Go", 20000, 80)
Python = Courses("Python", 18000, 60)

# 初始化学校
School1 = Schools("武当派", "武当山")
School2 = Schools("全真教", "终南山")
school_list = [School1, School2]

# 初始化学生
s1 = Students("大雄", 15, "M")
s2 = Students("胖虎", 17, "M")
s3 = Students("静香", 14, "F")
student_list = [s1, s2, s3]

# 初始化教师
t1 = Teachers("张三丰", 38, "M", Java)
t2 = Teachers("李清照", 35, "F", Go)
t3 = Teachers("王重阳", 45, "M", Python)
teacher_list = [t1, t2, t3]
