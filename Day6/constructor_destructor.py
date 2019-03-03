class Human(object):
    # 构造函数，用于对类的实例进行初始化（实例化）
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    def running(self):
        print("%s is running" % self.name)

    # 析构函数，用户类的实例销毁时执行清理动作
    def __del__(self):
        print("%s has gone" % self.name)


P1 = Human("Paul", 80, "male")
P2 = Human("Alice", 30, "female")

P1.running()
del P1  # 手工销毁
P2.running()  # 程序结束后自动销毁
