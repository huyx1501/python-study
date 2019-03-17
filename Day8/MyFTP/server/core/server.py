#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socketserver
import os
import yaml  # 用于解析配置文件


# 定义Handler类
class TCPHandler(socketserver.BaseRequestHandler):
    def put(self, filename):
        self.request.send(b"200")

    def get(self, filename):
        self.request.send(b"200")

    def pwd(self, *args):
        self.request.send(b"200")

    def ls(self, path=None):
        self.request.send(b"200")

    def cd(self, path):
        self.request.send(b"200")

    def handle(self):
        while True:
            try:
                message = self.request.recv(1024).encode().split()
                cmd = message[0]
                if hasattr(self, cmd):
                    func = getattr(self, cmd)
                    if len(message) > 1:
                        func(message[1])
                    else:
                        func()
                else:
                    self.request.send(b"400")  # 当命令不存在时返回错误代码400
            except (ConnectionResetError, ConnectionAbortedError) as e:
                print("客户端连接中断 ", e)
                break


def config_parser():
    """
    用于读取yaml格式中的配置文件内容
    :return: 返回读取到的配置内容
    """
    pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取程序根目录
    config_path = os.path.join(pwd, "config.yml")  # 组合配置文件路径
    if os.path.isfile(config_path):  # 确定配置文件存在并且是文件
        with open(config_path, "r") as f:
            return yaml.load(f, yaml.CLoader if yaml.CLoader else yaml.Loader)  # 读取并返回文件内容


def main():
    config = config_parser()  # 获取配置文件内容
    print(config)
    try:
        ip = str(config["server"]["bind"])  # 取出配置中的监听IP
        port = int(config["server"]["port"])  # 取出配置中的监听端口
        ftp_server = socketserver.ThreadingTCPServer((ip, port), TCPHandler)  # 实例化socketserver对象
        print("服务器启动，等待连接...")
        ftp_server.serve_forever()  # 开始监听
    except (ValueError, KeyError, TypeError) as e:
        print("配置文件有误，", e)
        exit(1)


if __name__ == "__main__":
    main()
