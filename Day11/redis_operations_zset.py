#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

pool = redis.ConnectionPool(host="192.168.80.10", port=6379, db=5)  # 创建一个redis连接池
r = redis.Redis(connection_pool=pool)  # 从连接池中申请连接

# 创建一个有序集合键或添加元素到有序集合
r.zadd("zset1", {"b": 10, "a": 20, "c": 30, "e": 40, "d": 50})  # 字典中key表示集合的元素，value表示元素的分值

# 获取集合中的元素数量
print("元素数量-->", r.zcard("zset1"))

# 获取集合中分值在指定范围内的元素数量
print("分值筛选-->", r.zcount("zset1", min=1, max=30))

# 增加指定元素的分数
r.zincrby("zset1", amount=50, value="a")

# 根据位置筛选
print("位置筛选-->", r.zrange("zset1", start=0, end=-1, withscores=True))

# 获取指定元素在集合中的位置
print("元素位置-->", r.zrank("zset1", "b"))

# 获取指定元素的分数
print("元素分数-->", r.zrank("zset1", "b"))

# 从集合中删除指定元素
r.zrem("zset1", "e")

# 根据位置范围删除元素
r.zadd("zset2", {"b": 10, "a": 21, "c": 13, "e": 34, "d": 5})
r.zremrangebyrank("zset2", min=1, max=3)  # 删除排行第1到3位的元素
print("按范围删除后-->", r.zrange("zset2", start=0, end=-1, withscores=True))

# 根据分数删除元素
r.zadd("zset3", {"b": 20, "a": 31, "c": 23, "e": 44, "d": 5})
r.zremrangebyscore("set3", min=20, max=30)  # 删除分数在20到30分之间的元素
print("按分数删除后-->", r.zrange("zset2", start=0, end=-1, withscores=True))

# 求两个有序集合的交集
"""
keys中字典key表示要做交集的集合名，value表示分数权重
aggregate表示合并时对分数的处理方式，可以是min,max,sum，每个集合元素的分数要乘以权重
"""
r.zinterstore(dest="zset4", keys={"zset2": 1, "zset3": 1.5}, aggregate="sum")

# 求两个集合的并集，参数用法和zinterstore一样
r.zunionstore(dest="zset5", keys={"zset2": 1, "zset3": 1.5}, aggregate="sum")

# 从集合键值中搜索符合条件的值, score_cast_func用于对分数进行处理
r.zadd("zset_names", {"Ward": 90, "Talbot": 65, "Fitz": 98, "Simmons": 96, "Daisy": 80, "Mack": 78, "May": 85, "Phil": 95})
print("搜索成员-->", r.zscan("zset_names", match="M*", count=1, score_cast_func=int))  # 返回元素的位置

# 迭代器方式搜索
items = r.zscan_iter("zset_names", match="M*")
print("第一次迭代-->", items.__next__())  # 返回元素内容
print("第二次迭代-->", items.__next__())