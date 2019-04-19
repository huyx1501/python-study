#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import selectors
import queue

def data_handler(source_data):
    """
    处理接收数据
    :param source_data: 源数据
    :return: 处理后的数据
    """
    return str(source_data).upper()


def connect(_server):
    """
    处理客户端连接
    :param _server: 接收连接的socket服务器对象
    :return: None
    """
    conn, addr = _server.accept()
    print("客户端连接已建立", addr)
    conn.setblocking(False)
    selector.register(conn, selectors.EVENT_READ, read)  # 将已建立的连接加入到selector事件监听列表，触发事件时调用read


def read(_conn):
    """
    接收并处理客户端数据
    :param _conn: 已与客户建立的连接对象
    :return: None
    """
    try:
        data = _conn.recv(1024).decode()
        if data:
            # _conn.sendall(r_data.encode())  # 发送数据
            data_queue.put(data)
            selector.unregister(_conn)  # 取消之前注册的EVENT_WRITE
            selector.register(_conn, selectors.EVENT_WRITE, send)  # 注册EVENT_WRITE
        else:
            print("客户端连接已断开", _conn.getpeername())
            selector.unregister(_conn)  # 取消当前连接的注册
    except ConnectionResetError:
        print("客户端连接已断开", _conn.getpeername())
        selector.unregister(_conn)  # 取消当前连接的注册


def send(_conn):
    data = data_queue.get()
    r_data = data_handler(data)  # 处理数据
    _conn.send(data.encode())
    _conn.send(r_data.encode())
    selector.unregister(_conn)  # 发送完毕，取消注册
    selector.register(_conn, selectors.EVENT_READ, read)  # 重新注册EVENT_READ事件


selector = selectors.DefaultSelector()  # 初始化一个selectors对象
data_queue = queue.Queue()
server = socket.socket()
server.bind(("0.0.0.0", 8888))
server.listen(1000)
server.setblocking(False)
print("服务器开始监听...")

selector.register(server, selectors.EVENT_READ, connect)  # 将socket对象注册到selectors，当触发事件时调用connect
while True:
    events = selector.select()  # 开始监听事件
    print(events)
    for key, mask in events:  #
        callback = key.data  # data为注册事件监听时传入的函数
        callback(key.fileobj)  # fileobj为传入的需要监听的对象，这里为socket服务器对象
