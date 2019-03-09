
class Dog(object):
    """
    这是Dog类的说明：
    此处省略5000字
    """
    def __init__(self, name):
        self.name = name

    def hello(self):
        print("Hello dog %s" % self.name)

    def __str__(self):
        return "这是一个Dog类"

    def __call__(self, *args, **kwargs):
        print("干嘛Call我？")


dog1 = Dog("小黄")
# __doc__属性表示类的描述
print(dog1.__doc__)
# __module__属性表示类所属的模块
print(dog1.__module__)
# __class__模块表示类（或实例）所属的类
print(dog1.__class__)
print(Dog.__class__)
# __dict__属性表示类中所有对象，以字典方式展示
print(dog1.__dict__)
print(Dog.__dict__)
# 如果在类中定义了__str__方法，则在打印实例时会获取__str__方法的返回值
print(dog1)
# 如果在类中定义了__call__方法，在对类的实例进行调用时会触发此方法
dog1()


# =========================自定义列表=====================
class CustomList(object):
    def __init__(self):
        self.data = {}  # 初始化一个空字典用于存储数据

    def __getitem__(self, item):
        return self.data.get(item)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]


# 实例化
list1 = CustomList()
# 触发__setitem__方法
list1["name"] = "Bob"
# 触发__getitem__方法
print(list1["name"])
# 触发__delitem__方法
del list1["name"]
print(list1["name"])