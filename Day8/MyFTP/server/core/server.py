#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socketserver
import os
import yaml  # 用于解析配置文件
import hashlib
import sys
import shutil


# 定义Handler类
class TCPHandler(socketserver.BaseRequestHandler):
    def auth(self):
        """
        用于进行远程用户认证
        :return: 认证通过返回用户信息
        """
        users = config["users"]
        self.request.send(b"Login")
        login_times = 0
        m = hashlib.md5()
        while login_times < 3:
            try:
                auth_data = self.request.recv(1024).decode().split()  # 接收认证消息
                user_info = users[auth_data[0]]  # 根据用户名查询用户信息
                if user_info:
                    password = user_info["key"]  # 取出用户密码
                    m.update(password.encode("utf-8"))
                    pass_md5 = m.hexdigest()
                    if pass_md5 == auth_data[1]:
                        pwd = user_info["home"]
                        config["users"][user_info["name"]]["pwd"] = pwd
                        self.request.send(("Success" + " " + pwd).encode("utf-8"))
                        return user_info["name"]
                    else:
                        self.request.send("密码错误".encode("utf-8"))
                        login_times += 1
            except KeyError:
                self.request.send("用户名不存在".encode("utf-8"))
                login_times += 1

    def put(self, user_info, params):
        """
        用户上传文件
        :param user_info: 已通过认证的用户属性
        :param params: 命令参数
        :return: None
        """
        user_pwd = user_info["pwd"]  # 用户当前工作目录
        username = user_info["name"]
        used_size = int(user_info["used"])  # 已用空间
        data_dir = config["server"]["data_dir"]  # 服务器数据目录
        filename = params[0]  # 第一个参数为文件名
        size = int(params[1])  # 第二个参数为文件大小
        user_quota = int(user_info["quota"])  # 用户磁盘配合
        print(user_quota)
        if used_size + size > user_quota:
            self.request.send("ERROR: 402 - 可用空间不足".encode("utf-8"))
            return
        filepath = os.path.join(data_dir, user_pwd, filename)  # 组合服务器数据目录，用户工作目录和文件名
        if os.path.isfile(filepath):
            self.request.send("ERROR: 409 - 资源已存在".encode("utf-8"))
        else:
            try:
                with open(filepath, "wb") as f:
                    self.request.send(b"200")  # 请求正确
                    received_size = 0
                    m = hashlib.md5()
                    while received_size < size:
                        if size - received_size > 1024:
                            buffer_size = 1024
                        else:
                            buffer_size = size - received_size
                        # 开始接收数据
                        _data = self.request.recv(buffer_size)
                        received_size += len(_data)
                        m.update(_data)
                        f.write(_data)
                    else:
                        md5sum = m.hexdigest()  # 计算md5
                        md5sum_client = self.request.recv(1024).decode("utf-8")  # 接收md5值
                        if md5sum == md5sum_client:
                            config["users"][username]["used"] += size  # 计算已使用空间
                            self.save()
                            print("文件[%s]接收成功，大小：[%s]，MD5：[%s]" % (filename, size, md5sum))
                        else:
                            os.remove(filepath)  # md5校验失败，删除文件
                            print("文件[%s]校验失败，源MD5：[%s] 本地MD5：[%s]" % (filename, md5sum_client, md5sum))
            except PermissionError:
                self.request.send("ERROR: 403 - 拒绝访问".encode("utf-8"))

    def get(self, user_info, params):
        """
        用户下载文件
        :param user_info: 已通过认证的用户属性
        :param params: 命令参数
        :return: None
        """
        user_pwd = user_info["pwd"]  # 用户当前工作目录
        data_dir = config["server"]["data_dir"]  # 服务器数据目录
        file = params[0]  # 第一个参数为文件名和相对路径
        filename = os.path.basename(file)
        filepath = os.path.join(data_dir, user_pwd, file)  # 组合服务器数据目录，用户工作目录和文件名
        if os.path.isfile(filepath):
            file_size = os.stat(filepath).st_size
            if file_size:
                self.request.send(str(file_size).encode("utf-8"))
                sent_size = int(self.request.recv(1024).decode("utf-8"))  # 等待客户端响应
                m = hashlib.md5()
                with open(filepath, "rb") as f:
                    if sent_size:  # 断点续传
                        f.seek(sent_size)
                        for line in f:
                            self.request.send(line)
                        md5sum = self.md5sum(filepath)  # 重新计算完整的md5值
                    else:
                        for line in f:
                            self.request.send(line)
                            m.update(line)
                        md5sum = m.hexdigest()
                self.request.send(md5sum.encode("utf-8"))
                print("文件[%s]发送完成" % filename)
            else:
                self.request.send("ERROR: 402 - 文件为空".encode("utf-8"))
        else:
            self.request.send("ERROR: 404 - 资源不存在".encode("utf-8"))

    def ls(self, user_info, *args):
        """
        获取目录或文件属性
        :param user_info: 已通过认证的用户属性
        :param args: 命令参数
        :return: None
        """
        if args:
            ls_path = args[0][0]
        else:
            ls_path = ""
        path = os.path.join(config["server"]["data_dir"], user_info["pwd"], ls_path)
        if platform == "win32":
            result = os.popen("dir " + path).read()
            result = result.replace(config["server"]["data_dir"], "")  # 去除结果中服务器数据目录
        else:
            result = os.popen("ls -lh" + path).read()
        if result:
            result_size = len(result.encode("utf-8"))
            self.request.send(str(result_size).encode("utf-8"))
            self.request.recv(1024)  # 等待客户端回应
            self.request.send(result.encode("utf-8"))
        else:
            self.request.send("0".encode("utf-8"))

    def cd(self, user_info, params):
        """
        用户切换工作目录
        :param user_info: 已通过认证的用户属性
        :param params: 命令参数
        :return: None
        """
        data_dir = config["server"]["data_dir"]
        username = user_info["name"]
        user_pwd = config["users"][username]["pwd"]  # 获取当前工作目录
        cd_path = params[0]
        path = os.path.join(data_dir, user_pwd, cd_path)
        if cd_path == "..":
            user_pwd = os.path.dirname(user_pwd)  # 获取上一级目录
            if not user_pwd:
                self.request.send("ERROR: 403 - 拒绝访问".encode("utf-8"))
            else:
                self.request.send(user_pwd.encode("utf-8"))
                config["users"][username]["pwd"] = user_pwd
        elif os.path.isdir(path):
            user_pwd = os.path.join(user_pwd, cd_path)
            config["users"][username]["pwd"] = user_pwd
            self.request.send(user_pwd.encode("utf-8"))
        else:
            self.request.send("ERROR: 404 - 无效的目录".encode("utf-8"))

    def mkdir(self, user_info, params):
        """
        在当前工作目录下创建目录
        :param user_info: 已通过认证的用户属性
        :param params: 命令参数
        :return: None
        """
        data_dir = config["server"]["data_dir"]
        username = user_info["name"]
        user_pwd = config["users"][username]["pwd"]  # 获取当前工作目录
        mk_path = params[0]
        path = os.path.join(data_dir, user_pwd, mk_path)
        if os.path.isdir(path):
            self.request.send("ERROR: 409 - 目录已存在".encode("utf-8"))
        else:
            os.makedirs(path)
            self.request.send("Success".encode())

    def rm(self, user_info, params):
        """
        删除目录或文件
        :param user_info: 已通过认证的用户属性
        :param params: 命令参数
        :return: None
        """
        data_dir = config["server"]["data_dir"]
        username = user_info["name"]
        user_pwd = config["users"][username]["pwd"]  # 获取当前工作目录
        rm_path = params[0]
        path = os.path.join(data_dir, user_pwd, rm_path)
        try:
            if os.path.isfile(path):
                size = os.stat(path).st_size
                os.remove(path)
                config["users"][username]["used"] -= size  # 释放空间，重新计算
                self.save()
                self.request.send("Success".encode())
            elif os.path.isdir(path):
                size = self.getsize(path)
                shutil.rmtree(path)
                if config["users"][username]["used"] - size < 0:
                    config["users"][username]["used"] = 0
                    self.save()
                else:
                    config["users"][username]["used"] -= size
                    self.save()
                self.request.send("Success".encode())
            else:
                self.request.send("ERROR: 404 - 目标不存在".encode("utf-8"))
        except PermissionError:
            self.request.send("ERROR: 403 - 拒绝访问".encode("utf-8"))

    def handle(self):
        print("连接已建立 %s" % str(self.client_address))
        try:
            auth_user = self.auth()  # 用户登陆并获取信息
            while auth_user:
                user_info = config["users"][auth_user]
                message = self.request.recv(1024).decode("utf-8").split()  # 获取客户端命令和参数
                cmd = message[0]
                if hasattr(self, cmd):  # 检查命令是否可用
                    func = getattr(self, cmd)
                    if len(message) > 1:
                        message.pop(0)
                        func(user_info, message)  # 有参数命令
                    else:
                        func(user_info)  # 无参数命令
                else:
                    self.request.send("ERROR: 405 - 无效的指令".encode("utf-8"))
        except (ConnectionResetError, ConnectionAbortedError, IndexError) as e:
            print("客户端连接中断...")
            return

    @staticmethod
    def getsize(path):
        """
        计算目录及其子目录的文件大小总和
        :param path: 目录名
        :return: 返回文件总大小
        """
        size = 0
        for root, dirs, files in os.walk(path):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return int(size)

    @staticmethod
    def save():
        """
        保存配置信息
        :return: None
        """
        server_info = config_parser()["server"]
        config["server"] = server_info # 服务器配置信息不要修改
        config["server"]["data_dir"] = "data" if server_info["data_dir"] is None else server_info["data_dir"]
        pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取程序根目录
        config_path = os.path.join(pwd, "config.yml")  # 组合配置文件路径
        if os.path.isfile(config_path):  # 确定配置文件存在并且是文件
            with open(config_path, "w") as f:
                yaml.dump(config, f)

    @staticmethod
    def md5sum(file):
        m = hashlib.md5()
        with open(file, "rb") as f:
            for line in f:
                m.update(line)
            return m.hexdigest()


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


def initial():
    """
    初始化用户目录
    :return: None
    """
    data_dir = config["server"]["data_dir"]
    if not (data_dir and os.path.isabs(data_dir)):  # 目录未配置或者未配置为绝对路径
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(root, data_dir if data_dir else "data")  # 默认数据目录为服务器根目录下的data
        config["server"]["data_dir"] = data_dir  # 将完整路径写入配置
    users = config["users"]
    for user in users:
        home_dir = users[user]["home"]  # 获取所有用户的家目录
        home_dir = os.path.join(data_dir, home_dir)
        if not os.path.isdir(home_dir):  # 目录不存在时为用户创建家目录
            os.makedirs(home_dir, mode=0o755)


def main():
    """
    主程序
    :return: None
    """
    global config, platform
    config = config_parser()  # 获取配置文件内容
    platform = sys.platform
    initial()
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
