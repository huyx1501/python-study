import random

# 随机返回一个0-1之间的浮点数
print("random: ", random.random())

# 随机返回一个指定数值之间的整数
print("randint: ", random.randint(0, 5))

# 随机返回一个range范围内的数值
print("randrange: ", random.randrange(5))
print("randrange: ", random.randrange(1, 3))   # 1，2

# 随机返回序列中的一个值，可以是字符串，列表，元组等
print("choice: ",random.choice("random"))

# 随机返回序列中的指定个数值
print("sample: ",random.sample("random", 2))

# 随机返回一个指定区间内的浮点数
print("uniform: ", random.uniform(1, 5))

# 打乱一个列表的排序
list1 = [1, 2, 3, 4, 5]
print("Before shuffle: ", list1)
random.shuffle(list1)
print("After shuffle: ", list1)