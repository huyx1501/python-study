#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika
import uuid
import time


class RpcClient(object):
    """
    RCP客户端
    """
    def __init__(self):
        self.uid = ""
        self.response = None
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.80.10"))
        self.channel = self.conn.channel()
        queue_tmp = self.channel.queue_declare(queue="", exclusive=True)  # 通过指定空白的队列名称来生成一个随机的queue
        self.callback_queue = queue_tmp.method.queue  # 获取队列名称
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.get_result, auto_ack=True)

    def get_result(self, ch, method, properties, body):
        """
        获取队列中的消息内容
        :param ch: 返回消息的通道名
        :param method:
        :param properties: 消息的附加属性
        :param body: 消息体
        :return: 返回数字形式的消息体
        """
        if properties.correlation_id == self.uid:
            self.response = int(body)

    def run(self, n):
        self.response = None  # 重置状态
        self.uid = str(uuid.uuid4())  # 生成本次消息的uid
        self.channel.basic_publish(exchange="",
                                   routing_key="rpc_queue",
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                   correlation_id=self.uid),
                                   body=str(n))
        while self.response is None:
            time.sleep(0.5)
            self.conn.process_data_events()  # 查询是否有新消息
        return self.response


Fib_RpcClient = RpcClient()
while True:
    try:
        num = int(input(">> "))
        print("获取第[%s]位斐波那契数列是[%s]" % (num, Fib_RpcClient.run(num)))
    except ValueError:
        print("非法输入，请输入一个正整数")
