class Human(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex


class Student(object):
    def __init__(self, school, course, score):
        self.school = school
        self.course = course
        self.score = score

    def studying(self):
        print("%s is studying at %s" % (self.name, self.school))


# 单继承
class Father(Human):
    def __init__(self, name, age, sex, kids):
        """super方法根据查找顺序（MRO）取查找符合的类调用，
        python2中经典类(class XXX:)为深度优先，新式类(class XXX(object):)为广度优先
        python3中为广度优先"""
        super().__init__(name, age, sex)  # Python2中应写为：super(Student, self)
        self.kids = kids


# 多继承
class Kids(Human, Student):
    # 重构父类的构造函数，增加属性
    def __init__(self, name, age, sex, school, course, score, father):
        # 调用父类的构造函数
        Human.__init__(self, name, age, sex)
        Student.__init__(self, school, course, score)

        self.father = father

    def playing(self):
        print("%s is playing with father %s" % (self.name, self.father))


f1 = Father("张全蛋", 40, "male", "张小明")
s1 = Kids("张小明", "15", "male", "铃兰高中", "数学", 80, "张全蛋")

# 调用类方法
s1.playing()
# 调用父类方法
s1.studying()

print(f1.name, f1.kids)
