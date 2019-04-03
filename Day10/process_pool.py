#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from multiprocessing import Lock, Pool
import time
import os


def func1(num):
    """
    提供给新进程调用的方法
    :param num: 传参
    :return: 返回子进程PID和执行时间
    """
    start_time = time.time()
    pid = os.getpid()
    time.sleep(1)
    print("[%s] output %s" % (pid, num))
    return [pid, time.time() - start_time]


def call_back1(args):
    """
    回调函数
    :param args: 进程执行的返回值作为回调函数的传参
    :return: None
    """
    print("进程[%s]用时[%s]秒" % (args[0], args[1]))


if __name__ == "__main__":
    pool = Pool(5)  # 创建进程池，指定进程池大小（即单次能执行的进程数）
    print("apply".center(30, "="))
    for i in range(2):
        pool.apply(func=func1, args=(i,))  # 串行
    print("apply_async".center(30, "="))
    for i in range(10, 20):
        pool.apply_async(func=func1, args=(i,), callback=call_back1)  # 异步并行,callback回调函数
    pool.close()
    pool.join()  # 进程池必须先close再join
