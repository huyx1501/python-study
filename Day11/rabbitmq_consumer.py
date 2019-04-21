#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.80.10"))
channel = connection.channel()
channel.queue_declare(queue="hello", durable=True)  # durable参数声明队列为持久化队列


def callback(ch, method, properties, body):
    print("Received message:")
    print("""ch: %s
method: %s
properties: %s
body: %s""" % (ch, method, properties, body))
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 如果没有自动确认则需手工调用确认方法
    print("Jod done")

"""
basic_consume参数:
queue: 要从哪个队列里接收消息
on_message_callback: 收到消息后的执行的回调函数，会传入四个参数channel,method,properties,body
auto_ack: 是否自定确认消息，如果不确认，消息会一直存在队列里不删除
"""
channel.basic_qos(prefetch_count=5)  # 指定缓存窗口大小，只有当缓存窗口未满时才会分发消息给消费者
channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=False)
print("Waiting for message.")
channel.start_consuming()
connection.close()
