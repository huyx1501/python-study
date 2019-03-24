#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import queue
import threading

print("Queue".center(50, "="))
q = queue.Queue(maxsize=3)  # 先进先出队列， maxsize设置队列最大长度
q.put("A")  # 存放元素
q.put("B")
q.put("C")
try:
    q.put("D", timeout=1)  # 如果不设置超时时间，向一个满的队列插入元素会阻塞
except queue.Full:
    print("Queue is full")
try:
    q.put_nowait("D")  # 不等待满队列空间释放，抛出queue.Full异常
except queue.Full:
    print("Queue is full")
print("Queue size: ", q.qsize())  # 查询队列大小
print(q.get())  # 获取队列中的元素
print(q.get())
print(q.get())
print("Queue size: ", q.qsize())
try:
    print(q.get(timeout=1))  # 如果不设置超时时间，取空队列会阻塞程序
except queue.Empty:
    print("Queue is empty")
try:
    print(q.get_nowait())  # 不等待空队列，抛出queue.Empty异常
except queue.Empty:
    print("Queue is empty")

# task_done: 且听下回分解

print("LifoQueue".center(50, "="))
ql = queue.LifoQueue()  # 后进先出队列
ql.put("A")
ql.put("B")
ql.put("C")
print(ql.get())  # 获取队列中的元素
print(ql.get())
print(ql.get())

print("PriorityQueue".center(50, "="))
qp = queue.PriorityQueue()  # 带优先级队列
qp.put((3, "A"))  # 通过插入元组方式指定优先级，数字越小，优先级越高，越快被取出
qp.put((1, "B"))
qp.put((2, "C"))
qp.put((-1, "D"))
print(qp.get())  # 获取队列中的元素
print(qp.get())
print(qp.get())
print(qp.get())
