#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from base_setup import *
from core import db_handler
import json


class MyHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.login_times = 0
        self.auth_user = None
        self.member_info = None
        self.menu = {}
        super().__init__(request, client_address, server)
        print("客户端已连接", self.client_address)

    def handle(self):
        while self.login_times < 3:  # 登陆失败次数达到3次中断连接
            try:
                if not self.auth_user:
                    # 接收认证数据
                    auth_data = json.loads(self.request.recv(1024).decode("utf-8"))
                    if self.auth(auth_data):
                        self.main()
                        break
                    else:
                        print("客户端登陆失败", str(self.client_address))
            except ConnectionResetError:
                print("客户端连接断开", self.client_address)
                break
        else:
            print("客户端登陆失败次数超过上限", str(self.client_address))

    def auth(self, auth_data):
        """
        进行用户验证
        :param auth_data:
        :return:
        """
        try:
            username = auth_data["username"]
            password = auth_data["password"]
        except KeyError:
            self.login_times += 1
            return False
        user = handler.get_user(name=username)
        if user:
            m_pass = user.password
            if password == m_pass:
                self.auth_user = user
                self.member_info = handler.get_member_info(user.member_id, user.role)
                # 认证成功发送用户信息到客户端，状态码200
                send_status = self.data_transfer([self.auth_user.__repr__(), self.member_info.__repr__()], 200)
                if send_status:
                    return True
                else:
                    return False
            else:
                self.login_times += 1
                self.data_transfer("密码错误", 403)  # 认证失败，状态码403
                return False
        else:
            self.login_times += 1
            self.data_transfer("用户名不存在", 403)  # 认证失败，状态码403
            return False

    def main(self):
        user_type = self.auth_user.role
        if user_type == 1:
            print("管理员[%s]已登陆" % self.member_info.name)
        elif user_type == 2:
            print("[%s]老师已登陆" % self.member_info.name)
        elif user_type == 3:
            print("[%s]同学已登陆" % self.member_info.name)
        else:
            exit("账户信息异常")
        menu = self.show_menu()
        self.data_transfer(menu)

    def show_menu(self, _pid=None):
        self.menu = handler.get_menu(self.auth_user.id, _pid)
        menu_list = []
        if self.menu:
            for mid, pid, code, name in self.menu:
                if pid == _pid:
                    menu_list.append({code: name})
            return menu_list
        else:
            return "没有有效权限"

    def data_transfer(self, data, code=200):
        """
        发送消息到客户端
        :param data: 要发送的消息，能被json序列号的类型
        :param code: 消息状态码，可参考HTTP协议
        :return: True Or False
        """
        try:
            if data or code:
                msg = json.dumps({
                    "code": code,
                    "data": data
                })
                # print(msg)
                msg_length = len(msg)
                self.request.sendall(str(msg_length).encode("utf-8"))
                ack = self.request.recv(1024)  # 等待客户端应答消息
                if not ack:
                    print("客户端连接断开", str(self.client_address))
                    return False
                self.request.sendall(msg.encode("utf-8"))
                return True
            else:
                print("非法数据")
                return False
        except TypeError as e:
            print("数据异常，发送失败", e)
            if local_server["debug"]:
                traceback.print_exc()
            return False


def main():
    global handler
    handler = db_handler.Handler()
    sms_server = socketserver.ThreadingTCPServer((local_server["bind_ip"], local_server["bind_port"]), MyHandler)
    print("服务器启动成功，等待连接...")
    sms_server.serve_forever()  # 开始监听


if __name__ == "__main__":
    main()

