#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import multiprocessing
import threading
import time
import os


def thread():
    print("Thread: ", os.getpid(), "  PPID: ", os.getppid())  # 打印PID和PPID(父进程PID)


def func():
    print("Process: ", threading.get_ident())  # 获取当前线程程ID
    time.sleep(2)
    sub = threading.Thread(target=thread)
    sub.start()


if __name__ == "__main__":
    for i in range(5):
        process = multiprocessing.Process(target=func)  # 定义新进程
        process.start()  # 启动进程
