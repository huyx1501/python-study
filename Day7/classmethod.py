class Dog(object):
    eyes = 2

    def __init__(self, name, eyes):
        self.name = name
        self.eyes = eyes

    # 类方法只能访问类变量，不能访问实例变量
    @classmethod
    def eye(cls):
        print("%s eyes" % cls.eyes)


dog1 = Dog("大黄", 3)
dog1.eye()
