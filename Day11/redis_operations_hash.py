#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

pool = redis.ConnectionPool(host="192.168.80.10", port=6379, db=2)  # 创建一个redis连接池
r = redis.Redis(connection_pool=pool)  # 从连接池中申请连接

# 设置一个hash键，键值以Key-Value的形式保存值
r.hset("info", "Name", "Bob")
r.hset("info", "Age", 18)
print(r.hget("info", "Mame"))  # 获取hash键值中指定的KEY值

# 批量设置hash键值中的K/V值
r.hmset("info", {"Country": "China", "Address": "Beijing", "Career": "Farmer", "Salary": 200})
print(r.hmget("info", {"Name", "Age"}))  # 批量获取hash键值中的KEY值

print(r.hgetall("info"))  # 获取键值中的所有KEY和Value

print(r.hlen("info"))  # 获取键值中Key的个数

print(r.hvals("info"))  # 获取键值中所有Key的Value

print(r.exists("info", "Age"))  # 判断键值中的Key是否存在

r.hdel("info", "Career")  # 删除键值中的某个Key

r.hincrby("info", "Salary", amount=10)  # 对数字类型的Key进行增量

r.hincrbyfloat("info", "Age", amount=1.5)  # 对数字类型的Key进行浮点数增量

print(r.hscan("info", cursor=0, match="A*"))  # 从键值中搜索符合添加的Key并返回其值

items = r.hscan_iter("info", match="A*")  # 创建一个搜索迭代器
print(items.__next__())
print(items.__next__())
