#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from multiprocessing import Process, Lock, freeze_support


def func(lock, num):
    lock.acquire()  # 申请锁
    print(num)
    lock.release()  # 释放锁

if __name__ == "__main__":
    plock = Lock()  # 创建进程锁
    for i in range(10):
        process = Process(target=func, args=(plock, i))  # 创建进程，传递锁
        process.start()