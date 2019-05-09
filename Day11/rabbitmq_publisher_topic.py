#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.80.10"))
channel = connection.channel()
channel.exchange_declare(exchange="info", exchange_type="topic")  # 声明一个exchange，类型为topic
try:
    while True:
        key = input("Key of the message: >>").strip()
        message = input("Something to send: >>").strip()
        channel.basic_publish(exchange="info", routing_key=key, body=message)
        print("Message sent")
finally:
    connection.close()
