#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from multiprocessing import Process, Manager


def func(d, l, n):
    d[n] = n + 1
    l.append(n + 1)


if __name__ == "__main__":
    manager = Manager()  # 创建Manager
    dic = manager.dict()  # 使用Manager创建一个可进程间共享的字典
    lst = manager.list()  # 使用Manager创建一个可进程间共享的列表
    process_list = []
    for i in range(5):
        process = Process(target=func, args=(dic, lst, i))  # 创建进程，传递Manager创建的字典和列表
        process.start()
        process_list.append(process)

    for p in process_list:
        p.join()

    print(dic)
    print(lst)
