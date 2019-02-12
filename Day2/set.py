# 去重
list_set1 = {1, 3, 5, 3, 2, 7, 9, 1}
print("list_set1", list_set1)

list_set2 = {2, 4, 6, 8, 1}

# 关系测试
# 差集
print("差集1：", list_set1.difference(list_set2))
print("差集2：", list_set2.difference(list_set1))

# 对称差集
print("对称差集：", list_set1.symmetric_difference(list_set2))

# 交集
print("交集：", list_set1.intersection(list_set2))

# 并集
print("并集：",list_set1.union(list_set2))

list_set3 = {1, 3}
# 子集
print("子集：", list_set3.issubset(list_set1))

# 父集
print("父集：", list_set1.issuperset(list_set3))

# 判断是否两集合无交集
list_set4 = {11, 23}
print("isdisjoint：", list_set1.isdisjoint(list_set4))

# 集合操作
# 移除交集
list_set1.difference_update(list_set2)
print("difference_update：", list_set1)

# 合并
list_set1.update(list_set2)
print("update：", list_set1)

# 移除指定项目：remove方法移除不存在元素会报错
list_set1.discard(10)
print("discard(10)：", list_set1)
list_set1.discard(9)
print("discard(9)：", list_set1)
