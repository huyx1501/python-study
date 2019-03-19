#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket


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
            if login_data:
                print("登陆成功！")
                cmd = input("[ %s/ ]# " % login_data)
        except ConnectionRefusedError:
            print("连接服务器失败...")
            exit(1)

    def download(self):
        pass

    def upload(self):
        pass

    def close(self):
        self.client.close()


client = FtpClient()
client.connect("127.0.0.1", 8888)
