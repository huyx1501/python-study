#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import redis

conn = redis.Redis(host="192.168.80.10")
channel = "ch1"  # 订阅的通道名
pub = conn.pubsub()  # 创建订阅者
pub.subscribe(channel)  # 订阅通道
pub.parse_response()  # 准备接收（处理第一条系统消息[b'subscribe', b'ch1', 1]）
while True:
    msg = pub.parse_response()  # 接收数据
    print(msg)
