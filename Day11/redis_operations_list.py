#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

pool = redis.ConnectionPool(host="192.168.80.10", port=6379, db=3)  # 创建一个redis连接池
r = redis.Redis(connection_pool=pool)  # 从连接池中申请连接

# 添加元素到List键的最左边（顶端）
r.lpush("Students", "Bob", "Tom", "Jerry", "Dennis")

# 添加元素到List键的最右边（末端）
r.rpush("Students", "Sam")

# 仅当List键存在时才添加元素到最左边
r.lpushx("Student", "Mario")

print(r.llen("Students"))  # 获取List键中值的个数

r.linsert("Student", where="BEFORE", refvalue="Tom", value="Sky")  # 在指定元素的指定位置插入值

r.lset("Students", index=1, value="Hunter")  # 修指定位置的元素

# 删除指定的值
r.lrem("Students", count=1, value="Jerry")

# 从List键顶部取出一个元素
r.lpop("Students")

# 从List键顶部取出一个元素
r.rpop("Students")

# 获取指定索引位置的元素
print(r.lindex("Student", index=0))

# 获取指定索引范围内的元素值
print(r.lrange("Students", start=0, end=-1))

r.lpush("Teachers", "Ward", "Talbot", "Fitz", "Simmons", "Daisy", "Mack", "May", "Phil")
r.ltrim("Teachers", start=2, end=6)  # 移除除指定索引范围内的所有元素

# 从一个List的末端取出一个元素，添加到另一个List的顶部
r.rpoplpush(src="Students", dst="Teachers")

# 从一个List的末端取出一个元素，添加到另一个List的顶部，在没有元素可取时等待超时时间
r.brpoplpush(src="Students", dst="Teachers", timeout=0)

# 从List最顶端取出一个元素，如果没有元素可取，等待超时时间
print(r.blpop("Teachers", timeout=2))

# 从List最末端取出一个元素，如果没有元素可取，等待超时时间
print(r.brpop("Teachers", timeout=2))
