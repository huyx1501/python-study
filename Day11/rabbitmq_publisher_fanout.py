#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.80.10"))  # 创建到RabbitMQ服务器的连接
channel = connection.channel()  # 创建通道
channel.exchange_declare(exchange="msg", exchange_type="fanout")  # 声明exchange名称和类型（fanout为广播模式）
message = ""
while message != "bye":
    message = input("Message to publish:>>")
    channel.basic_publish(exchange="msg", routing_key="", body=message)  # 发送消息到exchange进行分发
    print("Message sent")
connection.close()
