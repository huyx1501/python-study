import db_handler


class Schools(object):
    """
    学校类
    """
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.teachers = []
        self.students = []
        self.classes = []

    def registry(self, student, cls):
        self.students.append(student)
        print("[%s]注册成为[%s][%s%s]班学生成功" % (student.name, self.name, cls.teacher.name, cls.course.name))

    def hire(self, teacher):
        print("欢迎[%s]老师加入[%s]" % (teacher.name, self.name))
        self.teachers.append(teacher)
        self.classes.append(Classes(teacher.course.name, self, teacher.course, teacher))


class Classes(object):
    """
    班级类
    """
    def __init__(self, name, school, course, teacher):
        self.name = name
        self.school = school
        self.course = course
        self.teacher = teacher
        self.__open = 0

    @property
    def status(self):
        if self.__open == 0:
            return "下课中"
        if self.__open == 1:
            return "上课中"

    @status.setter
    def status(self, status):
        try:
            if int(status) == 0 or int(status) == 1:
                self.__open = int(status)
        except Exception as e:
            print("系统错误：", e)


class Courses(object):
    """
    课程类
    """
    def __init__(self, name, price, period):
        self.name = name
        self.price = price
        self.period = period


class Students(object):
    """
    学生类
    """
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    def chose_course(self):
        for i, school in enumerate(school_list):
            print("%s. %s" % (i+1, school.name))
        try:
            choice = input("请选择学校：")
            school = school_list[int(choice)-1]
            print(("%s课程表" % school.name) .center(50, "="))
            for i, item in enumerate(school.classes):
                print("%s. 课程：%s  费用：%s  讲师：%s" % (i + 1, item.name, item.course.price, item.teacher.name))
            choice = input("请选择课程：")
            cls = school.classes[int(choice)-1]
            print("请缴费%s元" % cls.course.price)
            tuition = input("请缴费：")
            if int(tuition) == cls.course.price:
                school.registry(self, cls)
            else:
                print("学费未缴清，注册失败")
        except ValueError as e:
            print("非法输入")
        except IndexError as e:
            print("选择的项目不存在")
        except Exception as e:
            print("注册失败,", e)


class Teachers(object):
    """
    教师类
    """
    def __init__(self, name, age, sex, course):
        self.name = name
        self.age = age
        self.sex = sex
        self.course = course

    def teaching(self):
        print("%s 正在教 %s" % (self.name, self.course))


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

# 初始化教师
t1 = Teachers("张三丰", 38, "M", Java)
t2 = Teachers("李清照", 35, "F", Go)
t3 = Teachers("王重阳", 45, "M", Python)

# 学校聘用教师
School1.hire(t1)
School1.hire(t2)
School2.hire(t3)

# 学生选课
s1.chose_course()
