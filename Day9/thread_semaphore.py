#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import threading
import time


def func(n):
    semaphore.acquire()  # 申请一个信号量
    print("Thread%s running" % n)
    time.sleep(1)
    semaphore.release()  # 释放一个信号量


semaphore = threading.BoundedSemaphore(3)  # 创建信号量
for i in range(10):
    thread = threading.Thread(target=func, args=(i,))
    thread.start()

while threading.active_count() != 1:
    print("Thread number ", threading.active_count())
    time.sleep(1)
else:
    print("Jobs done.")
