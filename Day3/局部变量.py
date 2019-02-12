# 定义全局变量
name = "Bob"
city = "Beijing"


def func1(_name):
    # 在函数内尝试重新定义全局变量
    name = _name
    # 函数内部访问全局变量city
    print("Welcome %s from %s" % (name, city))


# 调用
func1("Winner")
print("name after func1 in global:", name)
print("".center(20, "#"))


def func2(_name):
    # 声明全局变量city
    global city
    # 修改已声明全局变量city
    city = "Guangzhou"
    # 修改未声明全局变量name
    name = _name
    print("Welcome %s from %s" % (name, city))


func2("Winner")
print("name after func2 in global:", name)
print("city after func2 in global:", city)
print("".center(20, "#"))


list1 = ["Bob", "Winner", "Victor"]


def func3(_name):
    list1[0] = _name
    print(list1)


func3("Alex")
print("list1 after func3 in global:", list1)