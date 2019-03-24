#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import threading


def hello():
    thread_lock.acquire()  # 申请锁
    global n
    n += 1
    thread_lock.release()  # 释放锁


n = 0
thread_list = []
thread_lock = threading.Lock()  # 创建锁
for i in range(1000):
    thread = threading.Thread(target=hello)  # 创建线程
    thread.start()
    thread_list.append(thread)

for thread in thread_list:
    thread.join()  # 等待线程结束

print("Number: ", n)
