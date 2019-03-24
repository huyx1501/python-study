#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import threading
import queue
import time


class Producer(object):
    """生产者类"""
    def __init__(self, name, frequency=1):
        """
        生产者构造函数
        :param name: 生产者名称
        :param frequency: 生产频率（每秒生产的商品个数）
        """
        self.name = name
        self.frequency = frequency
        self.factory = threading.Thread(target=self.produce)  # 定义生产线程

    def produce(self):
        """生产者生产方法"""
        counter = 1
        while True:
            shop.put("%s-%s" % (self.name, counter))  # 存放商品到队列
            print("\033[1;32m[%s]生产了一个[%s-%s]\033[0m" % (self.name, self.name, counter))
            counter += 1
            time.sleep(1/self.frequency)


class Consumer(object):
    """
    消费者类
    """
    def __init__(self, name, frequency=1):
        """
        消费者构造函数
        :param name: 消费者名称
        :param frequency: 消费频率（每秒消费的商品个数）
        """
        self.name = name
        self.frequency = frequency
        self.shopping = threading.Thread(target=self.buy)  # 定义消费者线程

    def buy(self):
        """消费者消费方法"""
        while True:
            start_time = time.time()
            item = shop.get()  # 从队列取出商品
            print("\033[1;31m[%s]购买了[%s]\033[0m" % (self.name, item), " ", "等待时间: %.3f秒" % (time.time() - start_time))
            time.sleep(1/self.frequency)


shop = queue.Queue(maxsize=10)  # 定义队列
p1 = Producer("A1", 2)  # 定义生产者
p2 = Producer("A2", 3)
c1 = Consumer("Bob", 3)  # 定义消费者
c2 = Consumer("Tom", 1)
c3 = Consumer("Jerry", 2)

p1.factory.start()  # 启动生产者线程
p2.factory.start()
c1.shopping.start()  # 启动消费者线程
c2.shopping.start()
c3.shopping.start()
