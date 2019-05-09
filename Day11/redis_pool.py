#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

pool = redis.ConnectionPool(host="192.168.80.10", port=6379)  # 创建一个redis连接池
r = redis.Redis(connection_pool=pool)  # 从连接池中申请连接
r.set(2, "tom")
print(r.get(2))
