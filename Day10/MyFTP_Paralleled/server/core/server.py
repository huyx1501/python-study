#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import selectors
import yaml
import os
import sys
import shutil
import hashlib
import time
try:
    from yaml import CLoader as yaml_Loader
except ImportError:
    from yaml import Loader as yaml_Loader


class Server(object):
    def __init__(self, ip, port, backlog=1000):
        self.socket = socket.socket()
        self.socket.bind((ip, port))
        self.socket.listen(backlog)
        self.socket.setblocking(False)
        print("服务器启动，等待连接...")
        logger("服务器启动，等待连接...", "INFO")

    def accept(self):
        conn, addr = self.socket.accept()
        conn.setblocking(False)
        client = Connection(conn, addr)
        print("客户端连接已建立：%s" % str(addr))
        logger("客户端连接已建立：%s" % str(addr), "INFO", addr)
        selector.register(conn, selectors.EVENT_READ, client.handler)
        client.handler()


class Connection(object):
    def __init__(self, conn, addr):
        self.conn = conn  # 已建立的Socket连接
        self.addr = addr  # 客户端地址
        self.login_times = 0
        self.login = False  # 客户端是否已登录
        self.hello = False  # 是否已发送登录标志
        self.user = None  # 已验证用户信息
        self.state = {}
        self.reset()

    def reset(self):
        """
        重置状态
        :return: None
        """
        self.state["cmd"] = "cmd"
        self.state["cmd_state"] = None
        self.state["cmd_date"] = None
        self.state["opened_file"] = None
        self.state["filepath"] = ""
        self.state["temp_path"] = ""
        self.state["file_size"] = 0
        self.state["transferred_size"] = 0
        self.state["break"] = False
        self.state["md5"] = None

    def handler(self):
        if not self.login and not self.hello:
            self.conn.send(b"Login")
            self.hello = True
        elif not self.login and self.hello:
            self.auth()
        else:
            self.get_cmd()

    def auth(self):
        """
        用于进行远程用户认证，认证成功后绑定用户与连接
        :return: None
        """
        sep = os.sep
        users = config["users"]
        if self.login_times >= 3:
            logger("登陆失败次数达到上限", "ERROR", str(self.addr))
            selector.unregister(self.conn)
        if self.login_times < 3 and not self.login:
            m = hashlib.md5()
            auth_data = ""
            try:
                auth_data = self.conn.recv(1024).decode("utf-8").split()  # 接收认证消息
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
                        self.conn.send(("Success" + " " + pwd).encode("utf-8"))
                        self.user = config["users"][user_info["name"]]
                        self.login = True
                    else:
                        logger("用户[%s]登陆失败：密码错误" % auth_data[0], "ERROR", str(self.addr))
                        self.conn.send("密码错误".encode("utf-8"))
                        del m
                        self.login_times += 1
            except KeyError:
                logger("用户[%s]登陆失败：用户名不存在" % auth_data[0] if auth_data else "None", "ERROR", str(self.addr))
                self.conn.send("用户名不存在".encode("utf-8"))
                self.login_times += 1
            except (ConnectionResetError, ConnectionAbortedError) as e:
                logger("客户端连接中断：[%s]" % e, "WARN", str(self.addr))
                print("客户[%s]端连接中断..." % str(self.addr))
                selector.unregister(self.conn)

    def get_cmd(self):
        try:
            if not self.state["cmd_state"]:
                message = self.conn.recv(1024).decode("utf-8").split()  # 获取客户端命令和参数
                if not message:
                    logger("客户端连接中断", "WARN", str(self.addr))
                    print("客户[%s]端连接中断..." % str(self.addr))
                    selector.unregister(self.conn)
                    self.save()
                    return
                cmd = message[0]
                if hasattr(self, cmd):  # 检查命令是否可用
                    func = getattr(self, cmd)
                    if len(message) > 1:
                        message.pop(0)
                        func(message)  # 有参数命令
                    else:
                        func()  # 无参数命令
                else:
                    logger("ERROR: 405 - 无效的指令", "WARN", str(self.addr))
                    self.conn.send("ERROR: 405 - 无效的指令".encode("utf-8"))
            else:  # 非命令交互
                func = getattr(self, self.state["cmd"])
                func()
        except (ConnectionResetError, ConnectionAbortedError) as e:
            if self.state["opened_file"]:
                self.state["opened_file"].close()  # 发生异常时关闭打开的文件
            logger("客户端连接中断：[%s]" % e, "WARN", str(self.addr))
            print("客户[%s]端连接中断..." % str(self.addr))
            selector.unregister(self.conn)
            self.save()
        except AssertionError:
            if self.state["opened_file"]:
                self.state["opened_file"].close()  # 发生异常时关闭打开的文件
            self.conn.send("400".encode("utf-8"))  # 向客户端发送错误代码
            logger("文件[%s]发送失败" % os.path.basename(self.state["filepath"]), "ERROR", str(self.addr))
            print("客户[%s]接收文件失败..." % str(self.addr))
            self.reset()

    def put(self, *args):
        """
        用户上传文件
        :param args: 上传参数
        :return: None
        """
        if not self.state["cmd_state"]:
            user_pwd = self.user["pwd"]  # 用户当前工作目录
            used_size = int(self.user["used"])  # 已用空间
            data_dir = config["server"]["data_dir"]  # 服务器数据目录
            user_quota = int(self.user["quota"])  # 用户磁盘配合
            filename = args[0][0]  # 第一个参数为文件名
            file_size = self.state["file_size"] = int(args[0][1])  # 第二个参数为文件大小
            temp_file = filename + ".ftptemp"
            filepath = self.state["filepath"] = os.path.join(data_dir, user_pwd, filename)  # 组合服务器数据目录，用户工作目录和文件名
            temp_path = self.state["temp_path"] = os.path.join(data_dir, user_pwd, temp_file)  # 临时文件路径
            self.state["md5"] = hashlib.md5()
            if used_size + file_size > user_quota:
                logger("ERROR: 402 - 可用空间不足", "ERROR", str(self.addr))
                self.conn.send("ERROR: 402 - 可用空间不足".encode("utf-8"))
                return
            if os.path.isfile(filepath):
                logger("ERROR: 409 - 资源已存在：[%s]" % filename, "ERROR", str(self.addr))
                self.conn.send("ERROR: 409 - 资源已存在".encode("utf-8"))
                return
            if os.path.isfile(temp_path):
                self.state["transferred_size"] = os.stat(temp_path).st_size
                self.state["break"] = True
            self.conn.send(("200" + " " + str(self.state["transferred_size"])).encode("utf-8"))  # 返回请求状态和已接收大小
            self.state["cmd"] = "put"
            self.state["cmd_state"] = "wait_ack"
        else:
            file_size = self.state["file_size"]
            received_size = self.state["transferred_size"]
            temp_path = self.state["temp_path"]
            if not self.state["opened_file"]:
                self.state["opened_file"] = open(temp_path, "ab")  # 如果文件存在则追加，否则新建
            if file_size > received_size:
                if file_size - received_size > 1024:
                    buffer_size = 1024
                else:
                    buffer_size = file_size - received_size
                # 开始接收数据
                _data = self.conn.recv(buffer_size)
                self.state["transferred_size"] += len(_data)
                self.state["opened_file"].write(_data)
                if not self.state["break"]:
                    self.state["md5"].update(_data)
                self.state["opened_file"].flush()
                self.state["cmd_state"] = "received"
            else:
                self.state["opened_file"].close()
                # 计算md5，如果是断点续传则需要等接收完后重新计算
                md5sum_server = self.md5sum(self.state["temp_path"]) if self.state["break"] else self.state["md5"].hexdigest()
                md5sum_client = self.conn.recv(1024).decode("utf-8")  # 接收客户端源文件md5值
                filename = os.path.basename(self.state["filepath"])
                if md5sum_server == md5sum_client:
                    os.rename(self.state["temp_path"], self.state["filepath"])  # 接收完毕临时文件重命名为真实文件名
                    config["users"][self.user["name"]]["used"] += self.state["file_size"]  # 计算已使用空间
                    self.user = config["users"][self.user["name"]]  # 重新获取用户信息
                    info = "文件[%s]接收成功，大小：[%s]，MD5：[%s]" % (filename, self.state["file_size"], md5sum_server)
                    logger(info, "INFO", str(self.addr))
                    print(info)
                else:
                    os.remove(self.state["temp_path"])  # md5校验失败，删除文件
                    info = "文件[%s]校验失败，源MD5：[%s] 本地MD5：[%s]" % (filename, md5sum_client, md5sum_server)
                    logger(info, "ERROR", str(self.addr))
                    print(info)
                self.reset()  # 重置状态

    def get(self, *args):
        """
        用户下载文件
        :param args: 下载参数
        :return: None
        """
        if not self.state["cmd_state"]:
            user_pwd = self.user["pwd"]  # 用户当前工作目录
            data_dir = config["server"]["data_dir"]  # 服务器数据目录
            file = args[0][0]  # 第一个参数为文件名和相对路径
            filepath = self.state["filepath"] = os.path.join(data_dir, user_pwd, file)  # 组合服务器数据目录，用户工作目录和文件名
            if os.path.isfile(filepath):
                file_size = self.state["file_size"] = os.stat(filepath).st_size  # 计算文件大小
                if file_size:
                    self.conn.send(str(file_size).encode("utf-8"))
                    self.state["cmd"] = "get"
                    self.state["cmd_state"] = "wait_ack"
                    self.state["md5"] = hashlib.md5()
                else:
                    logger("ERROR: 402 - 文件为空", "ERROR", str(self.addr))
                    self.conn.send("ERROR: 402 - 文件为空".encode("utf-8"))
            else:
                logger("ERROR: 404 - 资源不存在：[%s]" % file, "ERROR", str(self.addr))
                self.conn.send("ERROR: 404 - 资源不存在".encode("utf-8"))
        else:
            file_size = self.state["file_size"]
            sent_size = self.state["transferred_size"]
            if file_size > sent_size:
                if not self.state["opened_file"]:
                    self.state["opened_file"] = open(self.state["filepath"], "rb")
                    self.state["transferred_size"] = int(self.conn.recv(1024).decode("utf-8"))  # 客户端回复已接收大小
                    if self.state["transferred_size"]:  # 处理断点续传
                        self.state["opened_file"].seek(self.state["transferred_size"])
                        self.state["break"] = True
                else:  # 正式发送文件时应该收到客户端的确认信号
                    ack = self.conn.recv(1024).decode("utf-8")
                    assert ack.strip() == "ACK"  # 断言收到的是"ACK"
                line = self.state["opened_file"].read(1024)  # 单次读取1024字节
                self.conn.send(line)  # 发送数据
                self.state["transferred_size"] += len(line)  # 累计已发送长度
                if not self.state["break"]:  # 非断点续传时每次接收都计算md5值
                    self.state["md5"].update(line)
            else:  # 文件传输完成处理后续任务
                self.conn.recv(1024)  # 最后一次ACK
                self.state["cmd_state"] = "sent_done"
                self.state["opened_file"].close()
                # 计算MD5值
                md5sum_server = self.md5sum(self.state["filepath"]) if self.state["break"] else self.state["md5"].hexdigest()
                self.conn.send(md5sum_server.encode("utf-8"))  # 发送MD5值
                filename = os.path.basename(self.state["filepath"])
                logger("文件[%s]发送完成" % filename, "INFO", str(self.addr))
                print("文件[%s]发送完成" % filename)
                self.reset()  # 重置状态

    def ls(self, *args):
        """
        获取目录或文件属性
        :param args: 命令参数
        :return: None
        """
        if not self.state["cmd_state"]:
            if args:
                ls_path = args[0][0]
            else:
                ls_path = ""
            data_dir = config["server"]["data_dir"]
            user_pwd = self.user["pwd"]  # 获取当前工作目录
            sep = os.sep
            ls_path = ls_path.replace("/", sep).replace("\\", sep)
            dirs = ls_path.split(sep)  # 拆分多级目录
            if ls_path.startswith(sep):  # 用户目录绝对绝对路径
                user_pwd = self.user["home"]
            for d in dirs:
                if d == "..":
                    user_pwd = os.path.dirname(user_pwd)  # 获取上一级目录
                    if not user_pwd:  # 已经没有上层了
                        logger("ERROR: 403 - 拒绝访问：[%s]" % ls_path, "ERROR", str(self.addr))
                        self.conn.send("ERROR: 403 - 拒绝访问".encode("utf-8"))
                        return
                else:
                    user_pwd = os.path.join(user_pwd, d)
            path = os.path.join(data_dir, user_pwd)
            if os.path.isfile(path) or os.path.isdir(path):  # 检查目录或文件是否存在
                if platform == "win32":
                    result = os.popen("dir " + path).read()
                    self.state["cmd_data"] = result.replace(config["server"]["data_dir"] + sep, "")  # 去除结果中服务器数据目录
                else:
                    self.state["cmd_data"] = os.popen("ls -lh" + path).read()
                if self.state["cmd_data"]:
                    result_size = len(self.state["cmd_data"].encode("utf-8"))
                    self.conn.send(str(result_size).encode("utf-8"))  # 发送结果集大小
                    self.state["cmd"] = "ls"
                    self.state["cmd_state"] = "wait_ack"
                else:
                    self.conn.send("目录为空".encode("utf-8"))
            else:
                logger("ERROR: 404 - 无效的文件或目录：[%s]" % ls_path, "ERROR", str(self.addr))
                self.conn.send("ERROR: 404 - 无效的文件或目录".encode("utf-8"))
        else:
                self.conn.recv(1024)  # 等待客户端回应
                self.conn.send(self.state["cmd_data"].encode("utf-8"))
                # 清除状态
                self.state["cmd"] = None
                self.state["cmd_state"] = None
                self.state["cmd_data"] = None

    def cd(self, params):
        """
        用户切换工作目录
        :param params: 命令参数
        :return: None
        """
        sep = os.sep
        data_dir = config["server"]["data_dir"]
        user_pwd = self.user["pwd"].rstrip(sep)  # 获取当前工作目录
        username = self.user["name"]
        cd_path = params[0]
        cd_path = cd_path.replace("/", sep).replace("\\", sep)
        dirs = cd_path.split(sep)  # 拆分多级目录
        if cd_path.startswith(sep):  # 用户目录绝对绝对路径
            user_pwd = self.user["home"].rstrip(sep)
        for d in dirs:
            if d == "..":
                user_pwd = os.path.dirname(user_pwd)  # 获取上一级目录
                if not user_pwd:  # 已经没有上层了
                    logger("ERROR: 403 - 拒绝访问非用户目录", "ERROR", str(self.addr))
                    self.conn.send("ERROR: 403 - 拒绝访问非用户目录".encode("utf-8"))
                    return
            else:
                user_pwd = os.path.join(user_pwd, d).rstrip(sep)
        path = os.path.join(data_dir, user_pwd)
        if os.path.isdir(path):
            config["users"][username]["pwd"] = user_pwd
            self.user = config["users"][self.user["name"]]  # 重新获取用户信息
            self.conn.send(user_pwd.encode("utf-8"))
            # self.save()
        else:
            logger("ERROR: 404 - 无效的目录：[%s]" % cd_path, "ERROR", str(self.addr))
            self.conn.send("ERROR: 404 - 无效的目录".encode("utf-8"))

    def mkdir(self, params):
        """
        在当前工作目录下创建目录
        :param params: 命令参数
        :return: None
        """
        data_dir = config["server"]["data_dir"]
        username = self.user["name"]
        user_pwd = config["users"][username]["pwd"]  # 获取当前工作目录
        mk_path = params[0]
        path = os.path.join(data_dir, user_pwd, mk_path)
        if os.path.isdir(path):
            logger("ERROR: 409 - 目录已存在：[%s]" % mk_path, "ERROR", str(self.addr))
            self.conn.send("ERROR: 409 - 目录已存在".encode("utf-8"))
        else:
            os.makedirs(path)
            logger("目录创建成功：[%s]" % mk_path, "INFO", str(self.addr))
            self.conn.send("Success".encode())

    def rm(self, params):
        """
        删除目录或文件
        :param params: 命令参数
        :return: None
        """
        data_dir = config["server"]["data_dir"]
        username = self.user["name"]
        user_pwd = config["users"][username]["pwd"]  # 获取当前工作目录
        rm_path = params[0]
        path = os.path.join(data_dir, user_pwd, rm_path)
        if os.path.isfile(path):
            size = os.stat(path).st_size
            os.remove(path)
            config["users"][username]["used"] -= size  # 释放空间，重新计算
            self.save()
            logger("文件删除成功：[%s]" % rm_path, "INFO", str(self.addr))
            self.conn.send("Success".encode())
        elif os.path.isdir(path):
            size = self.getsize(path)
            shutil.rmtree(path)
            if config["users"][username]["used"] - size < 0:
                config["users"][username]["used"] = 0
                self.user = config["users"][self.user["name"]]  # 重新获取用户信息
                # self.save()
            else:
                config["users"][username]["used"] -= size
                self.user = config["users"][self.user["name"]]  # 重新获取用户信息
                # self.save()
            logger("目录删除成功：[%s]" % rm_path, "INFO", str(self.addr))
            self.conn.send("Success".encode())
        else:
            logger("ERROR: 404 - 目标不存在：[%s]" % rm_path, "ERROR", str(self.addr))
            self.conn.send("ERROR: 404 - 目标不存在".encode("utf-8"))

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
            # self.user = config["users"][self.user["name"]]  # 重新获取用户信息
        else:
            exit("写入配置文件失败")

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


def config_parser():
    """
    用于读取yaml格式中的配置文件内容
    :return: 返回读取到的配置内容
    """
    config_path = os.path.join(root, "config.yml")  # 组合配置文件路径
    if os.path.isfile(config_path):  # 确定配置文件存在并且是文件
        with open(config_path, "r") as f:
            return yaml.load(f, yaml_Loader)  # 读取并返回文件内容


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


def main():
    """
    主程序
    :return: None
    """
    global platform, root, selector, config
    platform = sys.platform
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取程序根目录
    selector = selectors.DefaultSelector()
    config = config_parser()  # 获取配置文件内容
    initial()
    ip = str(config["server"]["bind"])  # 取出配置中的监听IP
    port = int(config["server"]["port"])  # 取出配置中的监听端口
    ftp_server = Server(ip, port, 1500)
    selector.register(ftp_server.socket, selectors.EVENT_READ, ftp_server.accept)
    while True:
        events = selector.select()  # 开始监听事件
        for key, mask in events:
            callback = key.data  # data为注册事件监听时传入的函数
            callback()


if __name__ == "__main__":
    main()
