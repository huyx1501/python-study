class Dog(object):
    def __init__(self, name):
        self.name = name

    def eat(self):
        print("%s is eating" % self.name)

    # 静态方法，不能使用类和实例的变量，与类唯一的关联只是需要通过类去调用
    @staticmethod
    def tips(self):
        print("name is %s" % self.name)


dog1 = Dog("小黄")
dog1.eat()
dog1.tips(dog1)  # 调用静态方法必须手工传递参数

