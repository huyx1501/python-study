#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import os

class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()
        self.auth_data = {}

    def __login(self, login_flag):
        login_time = 0
        while login_flag == "Login" and login_time < 3:
            try:
                self.auth_data["username"] = input("Login <username>: ").strip()
                self.auth_data["password"] = input("Login <password>: ")
                if self.auth_data["username"] and self.auth_data["password"]:  # 确定用户名密码已输入
                    self.client.send((self.auth_data["username"] + " " + self.auth_data["password"]).encode("utf-8"))
                    login_result = self.client.recv(1024).decode("utf-8")
                    if "Success" in login_result:
                        pwd = login_result.split()[1]
                        return pwd
                    else:
                        print("用户密码输入有误，请重新输入 : %s" % login_result)
                        login_time += 1
            except (ConnectionAbortedError, ConnectionResetError):
                print("登陆失败")
                break
        else:
            print("服务器异常，请联系管理员" if login_time < 3 else "登陆失败次数达到上限")

    def connect(self, server_ip, server_port):
        try:
            self.client.connect((server_ip, server_port))
            msg = self.client.recv(1024).decode()  # 等待服务器的发送登陆要求
            login_data = self.__login(msg)
            while login_data:
                input_data = input("[ %s/ ]# " % login_data).split()
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

    def put(self, *args):
        filename = args[0]
        if os.path.isfile(filename):
            file_size = os.stat(filename).st_size
            if file_size:
                cmd = "put %s %s" % (filename, file_size)
                self.client.send(cmd.encode("utf-8"))
                return_code = self.client.recv(1024).decode("utf-8")
                if return_code == "200":
                    sent_size = 0
                    with open(filename, "rb") as f:
                        for line in f:
                            self.client.send(line)
                            sent_size += len(line)
                        print("文件[%s]发送完成" % filename)
                else:
                    print("Error Code: %s" % return_code)
            else:
                print("无法上传空文件")
        else:
            print("无效的文件")

    def get(self):
        pass

    def ls(self):
        pass

    def delete(self):
        pass

    def cd(self):
        pass


client = FtpClient()
client.connect("127.0.0.1", 8888)
