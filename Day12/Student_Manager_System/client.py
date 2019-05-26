#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import hashlib
import json

# 服务器地址
server = {
    "host": "127.0.0.1",
    "port": 9999
}


class SmsClient(object):
    def __init__(self):
        self.client = socket.socket()
        self.login_times = 0
        self.auth_user = None
        self.member_info = None

    def main(self):
        try:
            self.client.connect((server["host"], server["port"]))
            print("连接服务器成功")
        except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as e:
            exit("连接服务器失败 %s" % e)
        while self.login_times < 3:
            if not self.member_info:
                print(self.login())
            else:
                print("[%s], 欢迎使用" % self.member_info["name"])
                break
        else:
            exit("登陆失败次数达到上限")

    def login(self):
        auth_data = dict()
        auth_data["username"] = input("请输入用户名：").strip()
        auth_data["password"] = self.get_md5(input("请输入密码："))
        if not auth_data["username"] or not auth_data["password"]:
            return "请输入账号密码"
        login_result = self.data_transfer(auth_data)
        # print(login_result)
        if login_result:
            if login_result["code"] == 200:
                self.auth_user = json.loads(login_result["data"][0].replace("'", "\"").replace("None", '""'))
                self.member_info = json.loads(login_result["data"][1].replace("'", "\"").replace("None", '""'))
                return "登陆成功"
            else:
                self.login_times += 1
                return login_result["data"]
        else:
            self.login_times += 1
            return "登陆失败"

    def data_transfer(self, msg):
        """
        发送消息到服务器并接收返回的内容
        :param msg: 要发送的消息，能被json序列号的类型
        :return: 返回收到的消息
        """
        try:
            msg = json.dumps(msg)
            self.client.sendall(msg.encode("utf-8"))
            result_length = int(self.client.recv(1024).decode("utf-8"))  # 服务器返回数据长度
            if result_length:
                self.client.sendall("ACK".encode("utf-8"))  # 发送应答报文
                result = ""
                received_size = 0
                if result_length - received_size > 1024:
                    buffer_size = 1024
                else:
                    buffer_size = result_length - received_size
                while received_size < result_length:
                    _data = self.client.recv(buffer_size).decode("utf-8")
                    received_size += len(_data)
                    result = result + _data
                # print(result)
                return json.loads(result)
            else:
                exit("服务器连接中断...")
        except (TypeError, ValueError) as e:
            print("数据包解析失败", e)
            return
        except (ConnectionAbortedError, ConnectionResetError, ConnectionError) as e:
            exit("服务器连接中断 %s" % e)

    @staticmethod
    def get_md5(data):
        m = hashlib.md5()
        m.update(data.encode("utf-8"))
        return m.hexdigest()


if __name__ == '__main__':
    sms_client = SmsClient()
    sms_client.main()
