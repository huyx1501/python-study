#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import os
import hashlib


class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()
        self.auth_data = {}

    def __login(self, login_flag):
        """
        用户登录接口
        :param login_flag: 服务器发送过来的第一个数据包
        :return: 登录成功返回当前工作目录
        """
        login_time = 0
        while login_flag == "Login" and login_time < 3:  # 正常服务器发送的第一个包应该是“Login”
            try:
                self.auth_data["username"] = input("Login <username>: ").strip()
                self.auth_data["password"] = input("Login <password>: ")
                if self.auth_data["username"] and self.auth_data["password"]:  # 确定用户名密码已输入
                    self.client.send((self.auth_data["username"] + " " + self.auth_data["password"]).encode("utf-8"))
                    login_result = self.client.recv(1024).decode("utf-8")  # 获取登录结果
                    if "Success" in login_result:
                        pwd = login_result.split()[1]
                        return pwd
                    else:
                        print("登录失败 : %s" % login_result)
                        login_time += 1
                else:
                    print("请输入用户名密码")
            except (ConnectionAbortedError, ConnectionResetError):
                print("登陆失败")
                break
        else:
            print("服务器异常，请联系管理员" if login_time < 3 else "登陆失败次数达到上限")

    def connect(self, server_ip, server_port):
        """
        客户端连接服务器的主接口
        :param server_ip: 服务器IP地址
        :param server_port: 服务器端口
        :return: None
        """
        try:
            self.client.connect((server_ip, server_port))  # 建立连接
            msg = self.client.recv(1024).decode()  # 等待服务器的发送登陆要求
            login_data = self.__login(msg)  # 登录
            while login_data:
                input_data = input("[ %s/ ]# " % login_data).split()  # 登录成功后显示命令行界面
                if not input_data:
                    continue
                cmd = input_data[0]
                if hasattr(self, cmd):
                    func = getattr(self, cmd)
                    if len(input_data) > 1:
                        func(input_data[1])
                    else:
                        func()
        except ConnectionRefusedError:
            print("连接服务器失败...")
            exit(1)

    def put(self, file):
        """
        上传文件接口
        :param file: 要上传的文件在本地的路径
        :return: None
        """
        filename = os.path.basename(file)  # 获取文件名
        if os.path.isfile(file):
            file_size = os.stat(file).st_size  # 获取文件大小
            if file_size:
                cmd = "put %s %s" % (filename, file_size)
                self.client.send(cmd.encode("utf-8"))
                return_code = self.client.recv(1024).decode("utf-8")
                if return_code == "200":
                    sent_size = 0
                    m = hashlib.md5()
                    with open(file, "rb") as f:
                        for line in f:
                            self.client.send(line)
                            sent_size += len(line)
                            m.update(line)
                        md5sum = m.hexdigest()  # 生成文件md5值
                        self.client.send(md5sum.encode("utf-8"))
                        print("文件[%s]发送完成" % filename)
                else:
                    print(return_code)
            else:
                print("无法上传空文件")
        else:
            print("无效的文件")

    def get(self):
        pass

    def ls(self, path=""):
        self.client.send(("ls" + " " + path).encode("utf-8"))
        result_size = int(self.client.recv(1024).decode("utf-8"))
        if result_size:
            self.client.send("ACK".encode("utf-8"))
            received_size = 0
            result = ""
            while received_size < result_size:
                if result_size - received_size > 1024:
                    buffer_size = 1024
                else:
                    buffer_size = result_size - received_size
                _result = self.client.recv(buffer_size)
                result += _result.decode("utf-8")
                received_size += len(_result)
            else:
                print(result)
        else:
            print("Nothing")

    def delete(self):
        pass

    def cd(self):
        pass


client = FtpClient()
client.connect("127.0.0.1", 8888)
