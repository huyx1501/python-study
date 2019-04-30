#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

pool = redis.ConnectionPool(host="192.168.80.10", port=6379, db=1)  # 创建一个redis连接池
r = redis.Redis(connection_pool=pool)  # 从连接池中申请连接

# 设置一个值, ex为过期时间（秒）, nx表示只有当key不存在时才新建
r.set(1, "a", ex=300, nx=True)
print(r.get(1))

# 同set的nx属性为True时
r.setnx(2, "b")
print(r.get(2))

# 设置新的键值和过期时间
r.setex(2, 600, "bb")
print(r.get(2))

# 按毫秒设置过期时间和键值
r.psetex(1, 600000, "aa")
print(r.get(1))

# 批量设置键值
r.mset({3: "c", 4: "d"})
print(r.mget(3, 4))  # 批量获取键值

# 返回旧值，设置新值
print(r.getset(1, "AA"))

# 从指定字符位置开始更新键值
r.setrange(1, 1, "1a2b3c4d")
print(r.getrange(1, 4, 6))

# 设置键值指定二进制位的值（0或1）
r.setbit(2, 1, 0)
print(r.get(2))

# 获取键值指定二进制位的值
print(r.getbit(2, 0))

# 统计键值二进制中1的个数
print(r.bitcount(1))

# 统计键值字符长度（UTF-8编码）
print(r.strlen(1))

# 在键值末尾追加字符串
r.append(3, "c3c3c3")
print(r.get(3))

r.set(5, 5)
# 对数字类的键值进行加增量操作
r.incr(5, 3)
print(r.get(5))

# 对数字类的键值进行加减量操作
r.decr(5, 2)
print(r.get(5))

# 对数字类的键值进行加增量操作（加浮点数）
r.incrbyfloat(5, 1.7)
print(r.get(5))
