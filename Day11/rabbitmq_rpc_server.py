#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika


def fib(n):
    """
    :param n: 位数
    :return: 返回第n位斐波那契数列
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def response(ch, method, pros, body):
    result = fib(int(body))  # 计算斐波那契数列
    # 发送消息到客户端指定的返回队列
    ch.basic_publish(exchange="",
                     routing_key=pros.reply_to,
                     properties=pika.BasicProperties(correlation_id=pros.correlation_id),
                     body=str(result))


connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.80.10"))
channel = connection.channel()
channel.queue_declare(queue="rpc_queue")
channel.basic_qos(prefetch_count=1)  # 指定缓存窗口大小，只有当缓存窗口未满时才会分发消息给消费者
channel.basic_consume(queue="rpc_queue", on_message_callback=response, auto_ack=True)  # 收到消息后交给response函数处理
print("Server started.")
channel.start_consuming()  # 接收客户端消息
connection.close()
