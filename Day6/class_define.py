# 定义类
class NewClass(object):
    # 类属性
    name = "Bob"

    # 类方法
    def prt(self):
        print("Hello", self.name)


# 定义一个类的实例
n1 = NewClass()
# 调用类属性和类方法
print(n1.name)
n1.prt()
