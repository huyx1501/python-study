#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socketserver
import os
import yaml  # 用于解析配置文件
import hashlib
import sys
import shutil
import time


# 定义Handler类
class TCPHandler(socketserver.BaseRequestHandler):
    def auth(self):
        """
        用于进行远程用户认证
        :return: 认证通过返回用户信息
        """
        sep = os.sep
        users = config["users"]
        self.request.send(b"Login")
        login_times = 0
        while login_times < 3:
            m = hashlib.md5()
            auth_data = self.request.recv(1024).decode().split()  # 接收认证消息
            try:
                user_info = users[auth_data[0]]  # 根据用户名查询用户信息
                if user_info:
                    password = user_info["key"]  # 取出用户密码
                    m.update(password.encode("utf-8"))
                    pass_md5 = m.hexdigest()
                    if pass_md5 == auth_data[1]:
                        pwd = config["users"][user_info["name"]]["pwd"].rstrip(sep)
                        if not pwd:  # pwd未设置
                            pwd = user_info["home"].rstrip(sep)
                            config["users"][user_info["name"]]["pwd"] = pwd
                        self.request.send(("Success" + " " + pwd).encode("utf-8"))
                        return user_info["name"]
                    else:
                        logger("用户[%s]登陆失败：密码错误" % auth_data[0], "ERROR", str(self.client_address))
                        self.request.send("密码错误".encode("utf-8"))
                        del m
                        login_times += 1
            except KeyError:
                logger("用户[%s]登陆失败：用户名不存在" % auth_data[0], "ERROR", str(self.client_address))
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
        user_quota = int(user_info["quota"])  # 用户磁盘配合
        filename = params[0]  # 第一个参数为文件名
        file_size = int(params[1])  # 第二个参数为文件大小
        temp_file = filename + ".ftptemp"
        filepath = os.path.join(data_dir, user_pwd, filename)  # 组合服务器数据目录，用户工作目录和文件名
        temp_path = os.path.join(data_dir, user_pwd, temp_file)  # 临时文件路径
        position = 0
        if used_size + file_size > user_quota:
            logger("ERROR: 402 - 可用空间不足", "ERROR", str(self.client_address))
            self.request.send("ERROR: 402 - 可用空间不足".encode("utf-8"))
            return
        if os.path.isfile(filepath):
            logger("ERROR: 409 - 资源已存在：[%s]" % filename, "ERROR", str(self.client_address))
            self.request.send("ERROR: 409 - 资源已存在".encode("utf-8"))
            return
        if os.path.isfile(temp_path):
            position = os.stat(temp_path).st_size
        received_size = position  # 已接收部分
        self.request.send(("200" + " " + str(received_size)).encode("utf-8"))  # 返回请求状态和已接收大小
        m = hashlib.md5()
        with open(temp_path, "ab") as f:  # 如果文件存在则追加，否则新建
            while received_size < file_size:
                if file_size - received_size > 1024:
                    buffer_size = 1024
                else:
                    buffer_size = file_size - received_size
                # 开始接收数据
                _data = self.request.recv(buffer_size)
                received_size += len(_data)
                f.write(_data)
                if not position:
                    m.update(_data)
            f.flush()
        md5sum_server = self.md5sum(temp_path) if position else m.hexdigest()  # 计算md5，如果是断点续传则需要等接收完后重新计算
        md5sum_client = self.request.recv(1024).decode("utf-8")  # 接收客户端源文件md5值
        if md5sum_server == md5sum_client:
            os.rename(temp_path, filepath)
            config["users"][username]["used"] += file_size  # 计算已使用空间
            self.save()  # 保存用户状态信息
            info = "文件[%s]接收成功，大小：[%s]，MD5：[%s]" % (filename, file_size, md5sum_server)
            logger(info, "INFO", str(self.client_address))
            print(info)
        else:
            os.remove(temp_path)  # md5校验失败，删除文件
            info = "文件[%s]校验失败，源MD5：[%s] 本地MD5：[%s]" % (filename, md5sum_client, md5sum_server)
            logger(info, "ERROR", str(self.client_address))
            print(info)

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
            file_size = os.stat(filepath).st_size  # 计算文件大小
            if file_size:
                self.request.send(str(file_size).encode("utf-8"))
                sent_size = int(self.request.recv(1024).decode("utf-8"))  # 客户端回复已接收大小
                m = hashlib.md5()
                with open(filepath, "rb") as f:
                    if sent_size:  # 断点续传
                        f.seek(sent_size)
                    for line in f:
                        self.request.send(line)
                        if not sent_size:  # 非断点续传时每次接收都计算md5值，避免重复打开文件
                            m.update(line)
                    f.flush()
                md5sum_client = self.md5sum(filepath) if sent_size else m.hexdigest()  # 计算md5，如果是断点续传则需要等接收完后重新计算
                self.request.send(md5sum_client.encode("utf-8"))
                logger("文件[%s]发送完成" % filename, "INFO", str(self.client_address))
                print("文件[%s]发送完成" % filename)
            else:
                logger("ERROR: 402 - 文件为空", "ERROR", str(self.client_address))
                self.request.send("ERROR: 402 - 文件为空".encode("utf-8"))
        else:
            logger("ERROR: 404 - 资源不存在：[%s]" % file, "ERROR", str(self.client_address))
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
        data_dir = config["server"]["data_dir"]
        user_pwd = user_info["pwd"]  # 获取当前工作目录
        username = user_info["name"]
        sep = os.sep
        ls_path = ls_path.replace("/", sep).replace("\\", sep)
        dirs = ls_path.split(sep)  # 拆分多级目录
        if ls_path.startswith(sep):  # 用户目录绝对绝对路径
            user_pwd = user_info["home"]
        for d in dirs:
            if d == "..":
                user_pwd = os.path.dirname(user_pwd)  # 获取上一级目录
                if not user_pwd:  # 已经没有上层了
                    logger("ERROR: 403 - 拒绝访问：[%s]" % ls_path, "ERROR", str(self.client_address))
                    self.request.send("ERROR: 403 - 拒绝访问".encode("utf-8"))
                    return
            else:
                user_pwd = os.path.join(user_pwd, d)
        path = os.path.join(data_dir, user_pwd)
        if os.path.isfile(path) or os.path.isdir(path):  # 检查目录或文件是否存在
            if platform == "win32":
                result = os.popen("dir " + path).read()
                result = result.replace(config["server"]["data_dir"] + sep, "")  # 去除结果中服务器数据目录
            else:
                result = os.popen("ls -lh" + path).read()
            if result:
                result_size = len(result.encode("utf-8"))
                self.request.send(str(result_size).encode("utf-8"))
                self.request.recv(1024)  # 等待客户端回应
                self.request.send(result.encode("utf-8"))
            else:
                self.request.send("目录为空".encode("utf-8"))
        else:
            logger("ERROR: 404 - 无效的文件或目录：[%s]" % ls_path, "ERROR", str(self.client_address))
            self.request.send("ERROR: 404 - 无效的文件或目录".encode("utf-8"))

    def cd(self, user_info, params):
        """
        用户切换工作目录
        :param user_info: 已通过认证的用户属性
        :param params: 命令参数
        :return: None
        """
        sep = os.sep
        data_dir = config["server"]["data_dir"]
        user_pwd = user_info["pwd"].rstrip(sep)  # 获取当前工作目录
        username = user_info["name"]
        cd_path = params[0]
        cd_path = cd_path.replace("/", sep).replace("\\", sep)
        dirs = cd_path.split(sep)  # 拆分多级目录
        if cd_path.startswith(sep):  # 用户目录绝对绝对路径
            user_pwd = user_info["home"].rstrip(sep)
        for d in dirs:
            if d == "..":
                user_pwd = os.path.dirname(user_pwd)  # 获取上一级目录
                if not user_pwd:  # 已经没有上层了
                    logger("ERROR: 403 - 拒绝访问非用户目录", "ERROR", str(self.client_address))
                    self.request.send("ERROR: 403 - 拒绝访问非用户目录".encode("utf-8"))
                    return
            else:
                user_pwd = os.path.join(user_pwd, d).rstrip(sep)
        path = os.path.join(data_dir, user_pwd)
        if os.path.isdir(path):
            config["users"][username]["pwd"] = user_pwd
            self.request.send(user_pwd.encode("utf-8"))
            self.save()
        else:
            logger("ERROR: 404 - 无效的目录：[%s]" % cd_path, "ERROR", str(self.client_address))
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
            logger("ERROR: 409 - 目录已存在：[%s]" % mk_path, "ERROR", str(self.client_address))
            self.request.send("ERROR: 409 - 目录已存在".encode("utf-8"))
        else:
            os.makedirs(path)
            logger("目录创建成功：[%s]" % mk_path, "INFO", str(self.client_address))
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
        if os.path.isfile(path):
            size = os.stat(path).st_size
            os.remove(path)
            config["users"][username]["used"] -= size  # 释放空间，重新计算
            self.save()
            logger("文件删除成功：[%s]" % rm_path, "INFO", str(self.client_address))
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
            logger("目录删除成功：[%s]" % rm_path, "INFO", str(self.client_address))
            self.request.send("Success".encode())
        else:
            logger("ERROR: 404 - 目标不存在：[%s]" % rm_path, "ERROR", str(self.client_address))
            self.request.send("ERROR: 404 - 目标不存在".encode("utf-8"))

    def handle(self):
        print("连接已建立 %s" % str(self.client_address))
        logger("连接已建立", "INFO", str(self.client_address))
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
                    logger("ERROR: 405 - 无效的指令", "WARN", str(self.client_address))
                    self.request.send("ERROR: 405 - 无效的指令".encode("utf-8"))
        except (ConnectionResetError, ConnectionAbortedError) as e:
            logger("客户端连接中断：[%s]" % e, "WARN", str(self.client_address))
            print("客户[%s]端连接中断..." % str(self.client_address))
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
        config_path = os.path.join(root, "config.yml")  # 组合配置文件路径
        if os.path.isfile(config_path):  # 确定配置文件存在并且是文件
            with open(config_path, "w") as f:
                yaml.dump(config, f)

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


def config_parser():
    """
    用于读取yaml格式中的配置文件内容
    :return: 返回读取到的配置内容
    """
    config_path = os.path.join(root, "config.yml")  # 组合配置文件路径
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
        data_dir = os.path.join(root, data_dir if data_dir else "data")  # 默认数据目录为服务器根目录下的data
        config["server"]["data_dir"] = data_dir  # 将完整路径写入配置
    users = config["users"]
    for user in users:
        home_dir = users[user]["home"]  # 获取所有用户的家目录
        home_dir = os.path.join(data_dir, home_dir)
        if not os.path.isdir(home_dir):  # 目录不存在时为用户创建家目录
            os.makedirs(home_dir, mode=0o755)
    log_dir = os.path.join(root, "logs")
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir, mode=0o755)
    logger("服务器初始化完成...", "INFO")


def logger(msg, level, client=None):
    """
    保存日志
    :param msg: 要保存的日志消息
    :param level: 日志级别
    :param client: 客户端地址
    :return: None
    """
    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_file = time.strftime("%Y-%m-%d", time.localtime()) + ".log"
    log_path = os.path.join(root, "logs", log_file)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("[%s] [%s] %s - %s" % (log_time, level, client if client else "-", msg.strip() + "\n"))


def main():
    """
    主程序
    :return: None
    """
    global config, platform, root
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取程序根目录
    config = config_parser()  # 获取配置文件内容
    platform = sys.platform
    initial()
    try:
        ip = str(config["server"]["bind"])  # 取出配置中的监听IP
        port = int(config["server"]["port"])  # 取出配置中的监听端口
        ftp_server = socketserver.ThreadingTCPServer((ip, port), TCPHandler)  # 实例化socketserver对象
        print("服务器启动，等待连接...")
        logger("服务器启动，等待连接...", "INFO")
        ftp_server.serve_forever()  # 开始监听
    except (ValueError, KeyError, TypeError) as e:
        logger("配置文件有误，服务器启动失败：%s" % e, "CRITICAL")
        print("配置文件有误，", e)
        exit(1)


if __name__ == "__main__":
    main()
