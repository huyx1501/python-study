#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import threading
import time


def func1():
    lock.acquire()
    global n
    n += 1
    print("func1 done")
    lock.release()


def func2():
    lock.acquire()
    global n
    n += 1
    print("func2 done")
    lock.release()


def main():
    lock.acquire()
    func1()
    func2()
    lock.release()


n = 0
lock = threading.RLock()  # 递归锁
# lock = threading.Lock()
t = threading.Thread(target=main)
t.start()

while threading.active_count() != 1:
    print(threading.active_count())  # 打印活跃线程数
    time.sleep(0.5)
else:
    print("Num: ", n)