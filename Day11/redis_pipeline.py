#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis
import time

pool = redis.ConnectionPool(host="192.168.80.10", port=6379, db=6)  # 创建一个redis连接池
r = redis.Redis(connection_pool=pool)  # 从连接池中申请连接

p = r.pipeline(transaction=True)  # 声明一个管道，可以将多个命令合并执行
p.set("1001", "aaa")  # 在管道中加入一个set命令
time.sleep(10)
p.set("1002", "bbb")
p.execute()  # 最终执行，将两次set一起完成，在此之前不会有值
