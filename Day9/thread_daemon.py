#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import threading
import time


def hello(n):
    print("Hello num %s" % n, threading.currentThread())
    time.sleep(1)
    print("Bye num %s" % n, threading.current_thread())


start_time = time.time()
thread_list = []
for i in range(50):
    thread = threading.Thread(target=hello, args=(i,), daemon=True)  # 设置为守护线程，主程序不用等子线程结束
    # thread.setDaemon(True)
    thread.start()
    thread_list.append(thread)

print("Jobs done in %s seconds" % (time.time() - start_time), threading.currentThread())
