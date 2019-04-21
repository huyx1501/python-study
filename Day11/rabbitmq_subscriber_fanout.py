#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.80.10"))
channel = connection.channel()
channel.exchange_declare(exchange="msg", exchange_type="fanout")  # 声明一个exchange并指定类型为fonout
result = channel.queue_declare(queue="", exclusive=True)  # 通过指定空白的队列名称来生成一个随机的queue,exclusive声明为唯一
queue_name = result.method.queue  # 获取队列名称
print("Queue name：", queue_name)
channel.queue_bind(exchange="msg", queue=queue_name)  # 将queue绑定到exchange


def callback(ch, method, properties, body):
    print("Received message:")
    print("""ch: %s
method: %s
properties: %s
body: %s""" % (ch, method, properties, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 如果没有自动确认则需手工调用确认方法
    print("Jod done")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
print("Waiting for message.")
channel.start_consuming()
connection.close()
