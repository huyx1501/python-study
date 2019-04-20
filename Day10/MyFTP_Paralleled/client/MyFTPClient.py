#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import os
import sys
import hashlib
import getpass


class FtpClient(object):
    """
    FTP客户端
    """
    def __init__(self):
        self.client = socket.socket()
        self.auth_data = {}
        self.login_data = {}

    def __login(self, login_flag):
        """
        用户登录接口
        :param login_flag: 服务器发送过来的第一个数据包
        :return: 登录成功返回当前工作目录
        """
        login_time = 0
        while login_flag == "Login" and login_time < 3:  # 正常服务器发送的第一个包应该是“Login”
            try:
                m = hashlib.md5()
                self.auth_data["username"] = input("Login <username>: ").strip()
                # self.auth_data["password"] = getpass.getpass("Login <password>: ")
                self.auth_data["password"] = input("Login <password>: ")  # 由于Pycharm不支持getpass模块，Pycharm调试时用input
                m.update(self.auth_data["password"].encode("utf-8"))
                if self.auth_data["username"] and self.auth_data["password"]:  # 确定用户名密码已输入
                    pass_md5 = m.hexdigest()  # 获取密码的MD5值
                    self.client.send((self.auth_data["username"] + " " + pass_md5).encode("utf-8"))
                    login_result = self.client.recv(1024).decode("utf-8")  # 获取登录结果
                    if "Success" in login_result:
                        pwd = login_result.split()[1]
                        return {"pwd": pwd}
                    else:
                        print("登录失败 : %s" % login_result)
                        del m
                        login_time += 1
                else:
                    print("请输入用户名密码")
            except (ConnectionAbortedError, ConnectionResetError):
                print("登陆失败")
                break
        else:
            print("服务器异常，请联系管理员" if login_time < 3 else "登陆失败次数达到上限")

    def getcmd(self):
        msg = self.client.recv(1024).decode()  # 等待服务器的发送登陆要求
        self.login_data = self.__login(msg)  # 调用登录接口
        while self.login_data:
            input_data = input("[ %s ]# " % self.login_data["pwd"]).split()  # 登录成功后显示命令行界面
            if not input_data:
                continue
            cmd = input_data[0]
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                if len(input_data) > 1:
                    func(input_data[1])
                else:
                    func()
            elif cmd == "bye":
                self.client.close()
                exit()

    def connect(self, server_ip, server_port):
        """
        客户端连接服务器的主接口
        :param server_ip: 服务器IP地址
        :param server_port: 服务器端口
        :return: None
        """
        try:
            self.client.connect((server_ip, server_port))  # 建立连接
        except ConnectionRefusedError:
            return False
        else:
            return True

    def put(self, file=None):
        """
        上传文件接口
        :param file: 要上传的文件在本地的路径
        :return: None
        """
        if not file:
            print("请指定要上传的文件")
            return
        filename = os.path.basename(file)  # 获取文件名
        if os.path.isfile(file):
            file_size = os.stat(file).st_size  # 获取文件大小
            if file_size:
                cmd = "put %s %s" % (filename, file_size)
                self.client.send(cmd.encode("utf-8"))
                return_data = self.client.recv(1024).decode("utf-8")  # 接收服务器返回
                if "200" in return_data:  # 正常返回
                    sent_size = int(return_data.split()[1])
                    position = sent_size
                    m = hashlib.md5()
                    with open(file, "rb") as f:
                        if position:  # 断点续传
                            f.seek(sent_size)
                        for line in f:
                            self.client.send(line)
                            sent_size += len(line)
                            if not position:
                                m.update(line)
                            percent = float(sent_size / file_size)
                            print("\r" + "[上传进度]: %s %.2f%%" % ("|" * int(percent*50), percent*100), end="")  # 打印进度条
                    md5sum_client = self.md5sum(file) if sent_size else m.hexdigest()  # 生成文件md5值
                    self.client.send(md5sum_client.encode("utf-8"))
                    print("")  # 进度条之后换行
                    print("文件[%s]发送完成" % filename)
                else:
                    print(return_data)
            else:
                print("无法上传空文件")
        else:
            print("无效的文件")

    def get(self, file=None):
        """
        下在服务器上的文件到本地
        :param file: 要下载的文件路径和文件名，如果不指定路径则默认当前目录
        :return:
        """
        if not file:
            print("请指定下载文件")
            return
        filename = os.path.basename(file)  # 提取文件名
        temp_file = filename + ".ftptemp"
        position = 0
        if os.path.isfile(temp_file):
            position = os.stat(temp_file).st_size  # 读取临时文件大小以确定已经接收的大小
        self.client.send(("get" + " " + file).encode("utf-8"))  # 发送指令
        data = self.client.recv(1024).decode("utf-8")  # 获取文件长度
        if data.isdigit():
            file_size = int(data)
            received_size = position  # 已接收部分
            self.client.send(str(received_size).encode("utf-8"))  # 回应已收到的文件长度
            m = hashlib.md5()
            with open(temp_file, "ab") as f:  # 如果已经存在在追加，否则新建
                while received_size < file_size:
                    if file_size - received_size > 1024:
                        buffer = 1024
                    else:
                        buffer = file_size - received_size
                    #  接收并保存数据
                    _data = self.client.recv(buffer)
                    if len(_data) == 3:
                        try:
                            if _data.decode("utf-8") == "400":
                                print("文件接收失败")
                                return
                        except UnicodeDecodeError:
                            pass
                    received_size += len(_data)
                    f.write(_data)
                    if not position:  # 非断点续传时每次接收都计算md5值，避免重复打开文件
                        m.update(_data)
                    percent = float(received_size / file_size)
                    print("\r" + "[下载进度]: %s %.2f%%" % ("|" * int(percent * 50), percent * 100), end="")  # 打印进度条
                    self.client.send("ACK".encode("utf-8"))  # 回复应答数据，准备下次接收
                f.flush()
            md5sum_client = self.md5sum(temp_file) if position else m.hexdigest()  # 计算md5，如果是断点续传则需要等接收完后重新计算
            md5sum_server = self.client.recv(1024).decode("utf-8")  # 接收服务器端源文件md5值
            if md5sum_client == md5sum_server:
                os.rename(temp_file, filename)
                print("")  # 进度条之后换行
                print("文件[%s]接收成功，大小：[%s]，MD5：[%s]" % (filename, file_size, md5sum_client))
            else:
                os.remove(temp_file)  # md5校验失败，删除文件
                print("")  # 进度条之后换行
                print("文件[%s]校验失败，源MD5：[%s] 本地MD5：[%s]" % (filename, md5sum_server, md5sum_client))
        else:
            print(data.strip())

    def ls(self, path=""):
        """
        列出服务器上当前所在工作目录的信息
        :param path: 指定路径
        :return: None
        """
        self.client.send(("ls" + " " + path).encode("utf-8"))
        result = self.client.recv(1024).decode("utf-8")
        if result.isdigit():
            result_size = int(result)
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
        else:
            print(result)

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
            if cd_path == ".":
                return
        self.client.send(("cd" + " " + cd_path).encode("utf-8"))  # 发送命令
        result = self.client.recv(1024).decode("utf-8")
        if "ERROR" in result:
            print(result.strip())
        else:
            self.login_data["pwd"] = result.strip()

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

    @staticmethod
    def md5sum(file):
        """
        计算整个文件的MD5值
        :param file: 要计算的文件
        :return: 返回文件MD5值
        """
        m = hashlib.md5()
        with open(file, "rb") as f:
            for line in f:
                m.update(line)
            return m.hexdigest()


if __name__ == "__main__":
    client = FtpClient()
    con = client.connect("127.0.0.1", 8888)
    if con:
        try:
            client.getcmd()
        except ConnectionResetError:
            exit("连接中断...")
    else:
        exit("连接服务器失败...")
