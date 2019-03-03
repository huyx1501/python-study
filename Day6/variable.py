class Dog(object):
    life = 20  # 类属性（变量）
    __legs = 4  # 私有属性，仅能内部调用

    # 构造函数
    def __init__(self, name, kind, color):
        # 初始化实例属性（变量）
        self.name = name
        self.kind = kind
        self.color = color

    def barking(self):
        print("%s Begin to shout" % self.name)
        self.__wang()  # 调用私有方法

    def running(self):
        print("%s is running with %s legs" % (self.name, self.__legs))  # 调用私有属性

    # 私有方法，仅能内部调用
    def __wang(self):
        print("%s Wang Wang Wang" % self.name)


# 定义两个实例
Husky = Dog("奇奇", "husky", "dark")
Chihuahua = Dog("吉吉", "chihuahua", "brown")

# 通过实例调用类变量（属性）
print("Husky.life: ", Husky.life)
# 重写类属性（等同于为实例添加属性）
Husky.life = 15
print("Husky.life: ", Husky.life)
# 原类属性不受影响
print("Dog.life: ", Dog.life)
Husky.barking()

# 其他实例仍然使用原来的类属性
print("Chihuahua.life: ", Chihuahua.life)
Chihuahua.running()
# 直接修改类属性
Dog.life = 12
print("Chihuahua.life: ", Chihuahua.life)
# 已经重写过该属性的实例不受影响
print("Husky.life: ", Husky.life)
