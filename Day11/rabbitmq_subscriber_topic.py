#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.80.10"))
channel = connection.channel()
channel.exchange_declare(exchange="info", exchange_type="topic")  # 声明一个exchange，类型为topic
result = channel.queue_declare(queue="", exclusive=True)  # 通过指定空白的队列名称来生成一个随机的queue,exclusive声明为唯一
queue_name = result.method.queue  # 获取队列名称
print("Queue name: ", queue_name)
keys = input("Your focus: >>").strip().split()  # 输入需要监听的内容，如*.info,、ssh.*、*.utils.*（单独一个#代表所有）
# 根据输入的监听内容，循环绑定routing_key到exchange中
for key in keys:
    channel.queue_bind(queue=queue_name, exchange="info", routing_key=key)


def callback(ch, method, properties, body):
    print("Received message:")
    print("""ch: %s
    method: %s
    properties: %s
    body: %s""" % (ch, method, properties, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 如果没有自动确认则需手工调用确认方法,method.delivery_tag为消息编号


channel.basic_consume(queue=queue_name, on_message_callback=callback)
print("Waiting for message.")
channel.start_consuming()
connection.close()
