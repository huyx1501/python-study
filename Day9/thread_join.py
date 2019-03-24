#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import threading
import time


def hello(n):
    print("Hello num %s" % n, threading.currentThread())  # currentThread或current_thread获取当前线程，
    time.sleep(1)
    print("Bye num %s" % n, threading.current_thread())


start_time = time.time()
thread_list = []
for i in range(50):
    thread = threading.Thread(target=hello, args=(i,))  # 创建线程
    thread.start()  # 启动线程
    thread_list.append(thread)

for t in thread_list:
    t.join()  # 等待子线程结束再往下执行

print("Jobs done in %s seconds" % (time.time() - start_time), threading.currentThread())
