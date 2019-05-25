#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from base_setup import *
from . import db_handler
import getpass

handler = db_handler.Handler()

user_data = {
    "username": "",
    "is_login": False,
    "user_info": None
}


def login():
    """
    用户登陆流程
    :return:   认证成功返回用户信息
    """
    login_count = 0
    while login_count < 3:
        name = input("请输入用户名：").strip()
        # password = getpass.getpass("Password:")
        password = input("Password:")
        user = handler.get_user(name=name)
        if user:
            m_pass = user.password
            if get_md5(password) == m_pass:
                user_data["is_login"] = True
                user_data["user_info"] = user
                return True
            else:
                print("密码不正确,请重试")
                login_count += 1
        else:
            print("用户名不存在,请重试")
            login_count += 1
    else:
        exit("登陆失败次数达到上限")


# 认证装饰器
def auth(func):
    def wrapper(*args, **kwargs):
        # 确定用户是否已登陆
        if user_data["is_login"]:
            # 已登陆用户直接执行调用的函数
            ret = func(*args, **kwargs)
            return ret
        else:
            # 调用登陆流程
            login_flag = login()
            if login_flag:
                ret = func(*args, **kwargs)
                return ret
    return wrapper

