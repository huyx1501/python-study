#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socketserver
import os
import yaml  # 用于解析配置文件


# 定义Handler类
class TCPHandler(socketserver.BaseRequestHandler):
    def auth(self, config):
        users = config["users"]
        self.request.send(b"Login")
        login_times = 0
        while login_times < 3:
            try:
                auth_data = self.request.recv(1024).decode().split()  # 接收认证消息
                user_info = users[auth_data[0]]  # 根据用户名查询用户信息
                if user_info:
                    password = user_info["key"]  # 取出用户密码
                    if password == auth_data[1]:
                        pwd = user_info["home"]
                        self.request.send(("Success" + " " + pwd).encode("utf-8"))
                        return user_info
                    else:
                        self.request.send("密码错误".encode("utf-8"))
                        login_times += 1
            except KeyError:
                self.request.send("用户名不存在".encode("utf-8"))
                login_times += 1

    def put(self, *args):
        if args:
            params = args[0]
            filename = params["filename"]
            size = params["size"]
            if os.path.isfile(filename):
                self.request.send(b"409")  # 资源已存在
            else:
                try:
                    with open(filename, "wb") as f:
                        self.request.send(b"200")  # 请求正确
                        received_size = 0
                        while received_size < size:
                            if size - received_size > 1024:
                                buffer_size = 1024
                            else:
                                buffer_size = size - received_size
                            # 开始接收数据
                            _data = self.request.recv(buffer_size)
                            received_size += len(_data)
                            f.write(_data)
                        else:
                            print("文件[%s]接收完成" % filename)
                except PermissionError:
                    self.request.send(b"403")  # 拒绝访问
        else:
            self.request.send(b"400")  # 命令参数有误

    def get(self, *args):
        self.request.send(b"200")

    def pwd(self, *args):
        self.request.send(b"200")

    def ls(self, path=None):
        self.request.send(b"200")

    def cd(self, *args):
        self.request.send(b"200")

    def handle(self):
        print("连接已建立 %s" % str(self.client_address))
        try:
            auth_data = self.auth(conf)  # 用户登陆并获取信息
            while auth_data:
                message = self.request.recv(1024).decode("utf-8").split()  # 获取客户端命令和参数
                cmd = message[0]
                if hasattr(self, cmd):  # 检查命令是否可用
                    func = getattr(self, cmd)
                    if len(message) > 1:
                        func(message[1])  # 有参数命令
                    else:
                        func()  # 无参数命令
                else:
                    self.request.send(b"405")  # 当命令不存在时返回错误代码405
        except (ConnectionResetError, ConnectionAbortedError, IndexError) as e:
            print("客户端连接中断...")
            return


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


def initial(config):
    data_dir = config["server"]["data_dir"]
    if not (data_dir and os.path.isabs(data_dir)):  # 目录未配置或者未配置为绝对路径
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(root, data_dir if data_dir else "data")  # 默认数据目录为服务器根目录下的data
    users = config["users"]
    for user in users:
        home_dir = users[user]["home"]  # 获取所有用户的家目录
        home_dir = os.path.join(data_dir, home_dir)
        if not os.path.isdir(home_dir):  # 目录不存在时为用户创建家目录
            os.makedirs(home_dir, mode=0o755)


def main(config):
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
    conf = config_parser()  # 获取配置文件内容
    initial(conf)
    main(conf)
