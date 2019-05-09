#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

conn = redis.Redis(host="192.168.80.10")
channel = "ch1"  # 发布的通道名
while True:
    msg = input(">> ")
    conn.publish(channel, msg)  # 发布消息到通道
