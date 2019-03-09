import db_handler


class Schools(object):
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.teachers = []
        self.students = []
        self.courses = []

    def registry(self, student):
            self.students.append(student)

    def hire(self, teacher):
        print("欢迎[%s]老师加入[%s]" % (teacher.name, self.name))
        self.teachers.append(teacher)
        self.courses.append(teacher.course)


class Courses(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Students(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    def chose_course(self):
        for school in db_handler.school_list():
            print("%s 课程表" % school.name .center(50, "="))
            for i, item in enumerate(school.courses):
                print("%s. 课程：%s  费用：%s" % (i + 1, item.name, item.price))
            choice = input("请选择课程：")
            if 0 < int(choice) <= len(school.courses):
                school.registry(self)


class Teachers(object):
    def __init__(self, name, age, sex, course):
        self.name = name
        self.age = age
        self.sex = sex
        self.course = course

    def teaching(self):
        print("%s 正在教 %s" % (self.name, self.course))


Java = Courses("Java", 15000)
Go = Courses("Go", 20000)
Python = Courses("Python", 18000)

School1 = Schools("武当派", "武当山")
School2 = Schools("全真教", "终南山")

s1 = Students("大雄", 15, "M")
s2 = Students("胖虎", 17, "M")
s3 = Students("静香", 14, "F")

t1 = Teachers("张三丰", 38, "M", Java)
t2 = Teachers("李清照", 35, "F", Go)
t3 = Teachers("王重阳", 45, "M", Python)

School1.hire(t1)
School1.hire(t2)
School2.hire(t3)


