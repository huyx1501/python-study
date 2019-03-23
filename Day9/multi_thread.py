#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import threading
import time


def hello(name):
    print("Hello %s" % name)
    time.sleep(1)
    print("Bye %s" % name)


# 创建线程
t1 = threading.Thread(target=hello, args=("Bob",))  # 创建线程
t2 = threading.Thread(target=hello, args=("Tom",))

# 启动线程
t1.start()  # 启动线程
t2.start()
