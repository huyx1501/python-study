#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

r = redis.Redis(host="192.168.80.10", port=6379)  # 创建一个redis连接
r.set(1, "bob")
print(r.get(1))
