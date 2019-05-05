#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

pool = redis.ConnectionPool(host="192.168.80.10", port=6379, db=4)  # 创建一个redis连接池
r = redis.Redis(connection_pool=pool)  # 从连接池中申请连接

# 创建一个集合键或添加元素到集合（自动去重）
r.sadd("set1", 1, 3, 5, 3, 8, 4, 2, 9, 1)

# 获取集合中元素的个数
print("元素个数-->", r.scard("set1"))

r.sadd("set2", 1, 3, 5, 3, 8)
# 返回在第一个集合中不在其他集合中的元素（差集）
print("差集-->", r.sdiff("set1", "set2"))

# 返回在第一个集合中不在其他集合中的元素并将结果存到另外一个集合
r.sdiffstore("set3", "set1", "set2")

# 求两个集合的交集
print("交集-->", r.sinter("set1", "set2"))

# 求两个集合的交集并将结果存到另外一个集合
r.sinterstore("set4", "set1", "set2")

# 求两个集合的并集
print("并集-->", r.sunion("set1", "set2"))

# 求两个集合的并集并将结果存到另外一个集合
r.sunionstore("set5", "set1", "set2")

# 判断值是否是集合成员
print("成员判断-->", r.sismember("set1", 1))

# 返回集合中的所有成员
print("获取所有成员-->", r.smembers("set1"))

# 将集合中的一个成员转移到另外一个集合
r.smove("set1", "set2", 2)

# 从集合的右侧（尾部）移除一个成员，并将其返回
print("尾部成员-->", r.spop("set2"))

# 从集合中随机获取多个元素
print("随机成员-->", r.srandmember("set1", 3))

# 从集合中删除指定的值（可以是多个）
r.srem("set1", 9)

# 从集合键值中搜索符合条件的值
r.sadd("set_names", "Ward", "Talbot", "Fitz", "Simmons", "Daisy", "Mack", "May", "Phil")
print("搜索成员-->", r.sscan("set_names", match="M*", count=1))  # 返回元素的位置

# 迭代器方式搜索
items = r.sscan_iter("set_names", match="M*")
print("第一次迭代-->", items.__next__())  # 返回元素内容
print("第二次迭代-->", items.__next__())
