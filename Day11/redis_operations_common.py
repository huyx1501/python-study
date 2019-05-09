#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

pool = redis.ConnectionPool(host="192.168.80.10", port=6379, db=0)  # 创建一个redis连接池
r = redis.Redis(connection_pool=pool)  # 从连接池中申请连接
r.mset({"1001": "aaaa", "1002": "bbbb", "1003": "cccc", "1004": "dddd", "1005": "eeee"})
r.mset({"1101": "aaaa", "1102": "bbbb", "1103": "cccc", "1104": "dddd", "1105": "eeee"})

# 删除键
r.delete("1005")

# 检测键是否存在
print(r.exists("1001"))
print(r.exists("1005"))

# 根据键名获取键值
print(r.keys("11*"))

# 设置键的超时时间（过期自动删除）
r.expire("1004", 600)

# 重命名键
r.rename("1104", "11004")

# 移动键到其他db
r.move("1003", 10)

# 随机获取一个键
print(r.randomkey())

# 返回指定键的数据类型
print(r.type("1001"))

# 搜索符合条件的键名
print(r.scan(match="1*2"))

# 迭代器方式搜索
items = r.scan_iter(match="1*2")
print("第一次迭代-->", items.__next__())  # 返回元素内容
print("第二次迭代-->", items.__next__())
