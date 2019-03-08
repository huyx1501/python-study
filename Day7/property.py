class Dog(object):
    def __init__(self, name, eyes):
        self.name = name
        self.food = "SS"

    # 属性方法，将一个方法转换成属性
    @property
    def hello(self):
        return "hello %s" % self.name

    # setter装饰器用于在设置对象属性时调用
    @hello.setter
    def hello(self, name):
        print("hello %s" % name)

    # deleter装饰器用于在删除对象时调用(实际上并不是删除属性方法本身)
    @hello.deleter
    def hello(self):
        del self.food


dog1 = Dog("大黄", 3)
print(dog1.hello)  # 属性方法不是一个可调用对象，不能使用()去调用
dog1.hello = "小黄"  # 为属性赋值，实际上是调用setter装饰的方法
del dog1.hello  # 删除属性，实际上是调用deleter装饰的方法
print(hasattr(dog1, "name"))
print(hasattr(dog1, "food"))  # 检查属性是否还存在
print(dog1.hello)
