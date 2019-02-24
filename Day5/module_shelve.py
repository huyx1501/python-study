import shelve


def func1():
    print("Message from func1")


# 使用shelve打开文件
d = shelve.open("shelve_dump")
# 以K/V形式存储值到对象d中
d["name"] = "Bob"
d["info"] = {"age":20, "addr": "CN"}
d["func"] = func1
d.close()

r = shelve.open("shelve_dump")
# .get方法获取指定元素
print(r.get("name"))
# .items方法获取所有元素
for item in r.items():
    print(item)
    # 还原函数
    if item[0] == "func":
        item[1]()
r.close()

