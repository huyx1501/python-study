#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.80.10"))
channel = connection.channel()
channel.queue_declare(queue="hello", durable=True)  # durable参数声明队列为持久化队列

data = ""
while not data == "bye":
    data = input("Something you want to publish: ")
    channel.basic_publish(exchange="", routing_key="hello", body=data,
                          properties=pika.BasicProperties(delivery_mode=2))  # delivery_mode指定消息持久化
    print("[INFO] - Message sent.")
connection.close()
