#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from multiprocessing import Process, Pipe


def func(con):
    print("Pipe in sub: ", con.recv())  # 从管道一端接收信息
    con.send("World")


if __name__ == "__main__":
    conn1, conn2 = Pipe()  # 创建管道，返回管道的两个节点
    p = Process(target=func, args=(conn2, ))  # 将其中一个节点传递给子进程
    p.start()
    conn1.send("Hello")  # 从管道一端发送信息
    print("Pipe in main: ",conn1.recv())

