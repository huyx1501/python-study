#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import os
import sys
import hashlib


class FtpClient(object):
    """
    FTP客户端
    """
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
                        return {"pwd": pwd}
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
            global login_data
            login_data = self.__login(msg)  # 登录
            while login_data:
                input_data = input("[ %s ]# " % login_data["pwd"]).split()  # 登录成功后显示命令行界面
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

    def get(self, file):
        """
        下在服务器上的文件到本地
        :param file: 要下载的文件路径和文件名，如果不指定路径则默认当前目录
        :return:
        """
        if not file:
            print("请指定下载文件")
            return
        filename = os.path.basename(file)  # 提取文件名
        self.client.send(("get" + " " + file).encode("utf-8"))  # 发送指令
        data = self.client.recv(1024).decode("utf-8")  # 获取文件长度
        if data.isdigit():
            file_size = int(data)
            self.client.send("ACK".encode("utf-8"))  # 回应收到文件长度
            received_size = 0
            m = hashlib.md5()
            with open(filename, "wb") as f:
                while received_size < file_size:
                    if file_size - received_size > 1024:
                        buffer = 1024
                    else:
                        buffer = file_size - received_size
                    #  接收并保存数据
                    _data = self.client.recv(buffer)
                    received_size += len(_data)
                    m.update(_data)
                    f.write(_data)
                else:
                    md5sum = m.hexdigest()  # 计算md5
                    md5sum_server = self.client.recv(1024).decode("utf-8")  # 接收md5值
                    if md5sum == md5sum_server:
                        print("文件[%s]接收成功，大小：[%s]，MD5：[%s]" % (filename, file_size, md5sum))
                    else:
                        os.remove(file)  # md5校验失败，删除文件
                        print("文件[%s]校验失败，源MD5：[%s] 本地MD5：[%s]" % (filename, md5sum_server, md5sum))
        else:
            print(data.strip())

    def ls(self, path=""):
        """
        列出服务器上当前所在工作目录的信息
        :param path: 指定路径
        :return: None
        """
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
                print(result.strip())
        else:
            print("Nothing")

    def rm(self, rm_path=""):
        """
        删除服务器上的目录或文件
        :param rm_path: 要删除的目标
        :return: None
        """
        if not rm_path:
            print("请指定要删除的目标")
            return
        else:
            self.client.send(("rm" + " " + rm_path).encode("utf-8"))
            result = self.client.recv(1024).decode("utf-8")
            if "ERROR" in result:
                print(result.strip())

    def cd(self, cd_path=""):
        """
        切换目录
        :param cd_path: 目标目录
        :return: None
        """
        if not cd_path:
            print("请指定切换目录")
            return
        else:
            cd_path = cd_path.strip("/").strip("\\")  # 去除最后的斜杠
            if cd_path == ".":
                return
        self.client.send(("cd" + " " + cd_path).encode("utf-8"))  # 发送命令
        result = self.client.recv(1024).decode("utf-8")
        if "ERROR" in result:
            print(result.strip())
        else:
            login_data["pwd"] = result.strip()

    def mkdir(self, mk_path=""):
        """
        创建一个空目录
        :param mk_path: 要创建的目录名
        :return:None
        """
        if not mk_path:
            print("请指定目录名")
            return
        else:
            self.client.send(("mkdir" + " " + mk_path).encode("utf-8"))
            result = self.client.recv(1024).decode("utf-8")
            if "ERROR" in result:
                print(result.strip())

    @staticmethod
    def lls(path=""):
        """
        列出本地目录信息
        :param path: 本地目录名
        :return: None
        """
        platform = sys.platform
        if platform == "win32":
            result = os.popen("dir " + path).read()
            print(result.strip())
        else:
            result = os.popen("ls " + path).read()
            print(result.strip())


client = FtpClient()
client.connect("127.0.0.1", 8888)
