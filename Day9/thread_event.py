#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import threading
import time


def light():
    """
    模拟红绿灯切换
    :return: None
    """
    event.set()  # 设置绿灯标志
    clock = 0  # 设置计数器
    while True:
        if clock < 5:  # 5秒内为绿灯时间
            print("\033[1;32mGreen light on...\033[0m")
            time.sleep(1)
            clock += 1
        elif 10 > clock >= 5:  # 5到10秒内清除绿灯标志
            event.clear()  # 清除绿灯，红灯亮
            print("\033[1;31mRed ligth on...\033[0m")
            time.sleep(1)
            clock += 1
        else:  # 超过10秒，重置计数器，重置绿灯
            clock = 0
            event.set()  # 设置红绿标志


def car(name):
    """
    模拟汽车等红绿灯
    :param name: 车名
    :return: None
    """
    while True:
        if event.is_set():  # 绿灯行
            print("\033[1;42m%s is running..." % name)
            time.sleep(1)
        else:  # 红灯停
            print("\033[1;41m%s stopped...\033[0m" % name)
            event.wait()  # 等绿灯亮
            print("\033[1;43m%s is ready to go..." % name)


event = threading.Event()  # 创建事件对象
thread_light = threading.Thread(target=light)  # 红绿灯线程
car_BMW = threading.Thread(target=car, args=("BMW", ))  # 车辆线程
thread_light.start()
car_BMW.start()
