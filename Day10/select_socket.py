#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import select
import queue


def data_handler(source_data):
    """
    处理接收数据
    :param source_data: 源数据
    :return: 处理后的数据
    """
    return str(source_data).upper()


server = socket.socket()
server.bind(("0.0.0.0", 8888))
server.listen(1000)
server.setblocking(False)  # 设为非阻塞的socket
print("服务器开始监听...")

inputs = []  # 接收监测
outputs = []  # 发送监测
send_data = {}  # 待发数据
inputs.append(server)  # 将socket服务加入监测列表

while inputs:
    # select参数为别为，读监测列表（接收），写监测列表（发送），异常列表
    read_list, write_list, exception_list = select.select(inputs, outputs, inputs)

    # 处理接收列表
    for item in read_list:
        if item is server:  # 服务器自身连接
            conn, addr = server.accept()
            print("客户端连接已建立", addr)
            inputs.append(conn)  # 将已建立的连接加入监测列表，等待客户端发数据时再接收
        else:  # 客户端连接
            try:
                data = item.recv(1024).decode()
                if not data:
                    print("客户端连接已断开", item.getpeername())
                    continue
                send_data[item] = queue.Queue()  # 创建本连接待发数据队列
                send_data[item].put(data)  # 将待发送数据放入队列
                outputs.append(item)  # 将当前连接放入待发送列表
            except ConnectionResetError:
                print("客户端连接已断开", item.getpeername())
                inputs.remove(item)  # 将断开的连接从监测列表删除

    # 处理待发送列表
    for item in write_list:
        try:
            data = send_data[item].get()  # 从队列提取数据
            r_data = data_handler(data)  # 处理数据
            item.sendall(r_data.encode())  # 发送数据给客户端
        except queue.Empty():
            pass
        except ConnectionResetError:
            print("客户端连接已断开", item.getpeername())
            del send_data[item]
        finally:
            outputs.remove(item)  # 处理完成后从待发列表删除当前连接

    # 处理异常列表
    for item in exception_list:
        inputs.remove(item)
        if item in outputs:
            outputs.remove(item)
