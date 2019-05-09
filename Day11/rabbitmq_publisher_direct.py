#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.80.10"))
channel = connection.channel()
channel.exchange_declare(exchange="logs", exchange_type="direct")  # 声明一个exchange，类型为direct
try:
    while True:
        level = input("Level of log: >>").strip()  # 消息级别，用作routing_key
        message = input("Message: >>").strip()
        channel.basic_publish(exchange="logs", routing_key=level, body=message)
        print("Message sent")
finally:
    connection.close()
