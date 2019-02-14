print("abs".center(20, "="))
# abs: 取绝对值
print(abs(-3))
print(abs(4))

print("all".center(20, "="))
# all: 如果一个可迭代对象中所有元素为真，返回真
print(all([0, 11, -4, True]))
print(all([1, 11, -4, True]))

print("any".center(20, "="))
# any: 如果一个可迭代对象中任一元素为真，返回真
print(any([0, 11, -4, True]))
print(any([1, 11, -4, False]))

print("bin".center(20, "="))
# bin: 整数转二进制
print(bin(16))

print("hex".center(20, "="))
# hex: 整数转十六进制
print(hex(18))

print("oct".center(20, "="))
# cot: 整数转八进制
print(oct(15))

print("bytearray".center(20, "="))
# bytearray: 可修改的bytes对象
ba = bytearray("abcde",encoding="utf-8")
print(ba,"ba[0]=%s" % ba[0])
ba[0] = 98
print(ba)

print("chr".center(20, "="))
# chr: 转换ascii编码为字符
print(chr(98))

print("ord".center(20, "="))
# ord: 转换字符为ascii编码
print(ord("b"))

print("dir".center(20, "="))
# dir: 查看对象的可用方法
list_a = [1, 2, 3]
print(dir(list_a))

print("enumerate".center(20, "="))
# enumerate: 返回一个可迭代对象的元素和元素的序号
dic_a = {"x": 12, "y": 83, "z": 61}
for n, m in enumerate(dic_a):
    print(n, m)

print("eval".center(20, "="))
# eval: 计算表达式
print(eval("1+2*3"))

print("filter".center(20, "="))
# filter: 从一组数据中过滤出符合条件的
fi = filter(lambda p: p > 5, range(10))
for i in fi:
    print(i)

print("map".center(20, "="))
# map: 讲后面的可迭代对象依次赋值给前面的函数
mp = map(lambda n: n*2, range(10))
print(type(mp))
for i in mp:
    print(i)

print("globals".center(20, "="))
# globals: 返回当前程序中的全局变量
print(globals())

print("locals".center(20, "="))
# locals: 返回函数内的局部变量
def test():
    local_var = "testing"
    print(locals())

test()


print("round".center(20, "="))
# round: 四舍五入
print(round(3.14159, 2))
print(round(3.6))

print("sorted".center(20, "="))
# sorted: 对无需的字典进行排序，返回列表
dic_b = {3: "a", 8: "c", 2: "e", 98: "g", 41: "n"}
print(dic_b)
print(sorted(dic_b))
print(sorted(dic_b.items()))  # 默认按key排序
print(sorted(dic_b.items(), key=lambda x: x[1]))  # 按value排序

print("zip".center(20, "="))
# zip: 组合两个列表的元素为两两一对的元组
list_b = [1, 2, 3, 4]
list_c = ["a", "b", "c", "d"]
for i in zip(list_b, list_c):
    print(i)

print("__import__".center(20, "="))
# __import__: 现在不清楚，以后再说。。。
__import__("progress")