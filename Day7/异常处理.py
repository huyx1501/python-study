list1 = ["a", "b", "c"]
try:
    print(list1[3])
except IndexError as e:  # 捕获指定异常类型，e为异常消息
    print("序号错误：", e)

dic1 = {"name": "Bob", "age": 16}
try:
    print(dic1["sex"])
except KeyError as e:  # 捕获指定异常类型，e为异常消息
    print("指定Key不存在：", e)


path = "C:\System Volume Information"  # 拒绝访问型
# path = "C:\aaa"  # 文件不存在型
# path = "Test"  # 正常打开型
try:
    with open(path, "r") as f:
        pass
except FileNotFoundError as e:  # 捕获指定异常类型，e为异常消息
    print("打开文件失败：", e)
except PermissionError as e:  # 捕获指定异常类型，e为异常消息
    print("拒绝访问：", e)
except Exception as e:  # 捕获所有异常类型，e为异常消息
    print("出错了：", e)
else:  # 当没有异常时的操作
    print("打开文件成功")
finally:  # 无论是否有异常都会执行的操作
    print("操作完成")


# 自定义错误类型
class MyException(Exception):
    pass

try:
    raise MyException("系统错误。。。。。")  # 手工触发错误
except MyException as e:
    print(e)