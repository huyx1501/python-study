class Dog(object):
    def __init__(self, name):
        self.name = name

    def eat(self):
        print("%s is eating" % self.name)


dog1 = Dog("小黄")


def walk(self):
    print("%s is walking" % self.name)


# hasattr方法判断对象中是否存在指定属性或方法
print(hasattr(dog1, "eat"))
print(hasattr(dog1, "walk"))

# getattr方法根据字符串在对象中查找并返回匹配的属性或方法
print(getattr(dog1, "eat"))  # 返回函数eat的内存地址
# print(getattr(dog1,"walk"))  # 不存在的属性或方法会报错

# setattr方法设置对象的新属性或方法（方法需要传递一个函数的内存地址）
setattr(dog1, "run", walk)
dog1.run(dog1)

k = input("Key:")
v = input("Value:")
setattr(dog1, k, v)
print(getattr(dog1, k))  # 获取属性，直接返回属性值

# delattr 方法用于删除对象中匹配的方法或属性(不能删除继承的方法)
delattr(dog1, "eat")
print(hasattr(dog1, "eat"))