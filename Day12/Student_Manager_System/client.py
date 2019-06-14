#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket
import hashlib
import json
import traceback

# 服务器地址
server = {
    "host": "127.0.0.1",
    "port": 9999,
    "debug": True
}


class SmsClient(object):
    def __init__(self):
        self.client = socket.socket()
        self.login_times = 0
        self.auth_user = None
        self.member_info = None
        self.menu = None
        self.current_menu = []
        self.position = None

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
                self.show_menu()  # 显示主菜单
                self.interaction()  # 开始交互
                break
        else:
            exit("登陆失败次数达到上限")

    def login(self):
        auth_data = dict()
        auth_data["username"] = input("请输入用户名：").strip()
        auth_data["password"] = self.get_md5(input("请输入密码："))
        if not auth_data["username"] or not auth_data["password"]:
            return "请输入账号密码"
        self.client.sendall(json.dumps(auth_data).encode("utf-8"))
        login_result = self.get_response()
        # print(login_result)
        if login_result:
            if login_result["code"] == 200:
                self.auth_user = json.loads(login_result["data"][0].replace("'", "\"").replace("None", '""'))
                self.member_info = json.loads(login_result["data"][1].replace("'", "\"").replace("None", '""'))
                self.menu = login_result["data"][2]
                return "登陆成功"
            else:
                self.login_times += 1
                return login_result["data"]
        else:
            self.login_times += 1
            return "登陆失败"

    def show_menu(self):
        self.current_menu.clear()
        for menu in self.menu:
            if menu[1] == self.position:  # 仅显示当前位置下的子菜单
                self.current_menu.append(menu)
        if self.current_menu:
            for i, m in enumerate(self.current_menu):
                print("%d: %s" % (i + 1, m[3]))
            else:
                if self.current_menu[0][1]:  # 存在PID则显示返回上一级
                    print("%d: %s" % (len(self.current_menu) + 1, "返回上一级"))
                    print("%d: %s" % (len(self.current_menu) + 2, "返回主菜单"))
        else:
            print("无可用菜单！")
            if self.current_menu[0][1]:  # 存在PID则显示返回上一级
                print("%d: %s" % (len(self.current_menu) + 1, "返回上一级"))
                print("%d: %s" % (len(self.current_menu) + 2, "返回主菜单"))

    def interaction(self):
        while True:
            try:
                choice = int(input(">> "))
                if choice == len(self.current_menu) + 1:  # 返回上一级
                    for menu in self.menu:
                        if menu[0] == self.position:  # 找出当前位置的菜单
                            self.position = menu[1]  # 获取当前位置菜单的上级菜单ID
                    self.show_menu()
                    continue
                elif choice == len(self.current_menu) + 2:  # 返回主菜单:
                    self.position = None
                    self.show_menu()
                    continue
                else:
                    choice_menu = self.current_menu[choice - 1]  # 获取选择的菜单项
                if choice_menu[2]:  # 子菜单是最终菜单（菜单中有code项）
                    cmd = input("# ").strip()
                    data = choice_menu[2] + " " + cmd
                    self.client.sendall(data.encode("utf-8"))
                    result = self.get_response()
                    if result["code"] == 200:
                        print(result["data"])
                    else:
                        print("错误代码[%d]：%s" % (result["code"], result["data"]))
                    self.show_menu()  # 重新显示最后一层的菜单
                else:
                    self.position = choice_menu[0]  # 获取菜单项中的ID
                    self.show_menu()  # 显示下级菜单
            except (ValueError, IndexError):
                print("无效选择，请重新输入")

    def get_response(self):
        """
        接收服务器消息
        :return: 返回收到的消息
        """
        try:
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
            if server["debug"]:
                traceback.print_exc()
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
