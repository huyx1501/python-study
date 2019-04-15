#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob


import gevent


def func1():
    print("func1 first")
    gevent.sleep(2)  # 模拟IO延迟
    print("func1 second")
    gevent.sleep(1)
    print("func1 third")


def func2():
    print("func2 first")
    gevent.sleep(1)
    print("func2 second")
    gevent.sleep(1)
    print("func2 third")


def func3():
    print("func3 first")
    gevent.sleep(0)
    print("func3 second")
    gevent.sleep(1)
    print("func3 third")


# 等待所有函数执行结束
gevent.joinall([
    gevent.spawn(func1),  # 将函数加入greenlet调度
    gevent.spawn(func2),
    gevent.spawn(func3),
])