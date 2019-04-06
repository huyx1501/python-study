#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import gevent
from gevent import monkey
monkey.patch_all()  # # 引入monkey补丁，使标准库对gevent友好


def handler(conn, addr):
    """
    处理客户端连接
    :param conn: 客户端连接对象
    :param addr: 客户端地址
    :return: None
    """
    print("Accept connection from ", addr)
    try:
        while True:
            data = conn.recv(1024).decode()
            print(data)
            conn.send("OK".encode())
    except Exception as e:
        print("连接断开 ", e)
    finally:
        conn.close()


def server(port):
    """
    在指定端口建立socket监听，并使用gevent协程非阻塞地处理客户端连接
    :param port: 服务器监听端口
    :return: None
    """
    s_server = socket.socket()  # 创建socket对象
    s_server.bind(("0.0.0.0", port))
    s_server.listen(100)  # 监听
    print("Listening on port %s ..." % port)
    while True:
        conn, addr = s_server.accept()
        gevent.spawn(handler, conn, addr)  # 利用gevent创建客户端连接处理协程


server(8888)
