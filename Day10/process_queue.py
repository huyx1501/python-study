#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from multiprocessing import Process, Queue


def func1(queue):
    queue.put("World")  # 往队列存放数据


def func2(queue):
    while queue.qsize() > 0:
        print("Get item from queue: ", queue.get())  # 从队列取数据


if __name__ == "__main__":
    q = Queue()
    q.put("Hello")
    p1 = Process(target=func1, args=(q, ))
    p2 = Process(target=func2, args=(q, ))
    p1.start()
    p2.start()
