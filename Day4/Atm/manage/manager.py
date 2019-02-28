import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from conf import config
from db import db_controller
from main import logger

admin_status = {
    "login_flag":  False
}


def login():
    """
    登陆流程
    :return: 登陆成功返回True
    """
    login_count = 0
    info = config.manager
    while login_count < 3:
        name = input("Username：")
        password = input("Password:")
        if name == info["username"] and password == info["password"]:
            admin_status["login_flag"] = True
            return True
        else:
            print("登录失败")
            login_count += 1
    else:
        print("登陆失败次数达到上限")


# 认证装饰器
def auth(func):
    def wrapper(*args, **kwargs):
        # 确定用户是否已登陆
        if admin_status["login_flag"]:
            # 已登陆用户直接执行调用的函数
            func(*args, **kwargs)
        else:
            # 调用登陆流程
            login_flag = login()
            if login_flag:
                func(*args, **kwargs)
            else:
                exit(1)
    return wrapper


@auth
def user_add():
    """
    添加新用户
    :return:
    """
    pass


@auth
def user_query():
    """
    查询用户信息
    :return:
    """
    pass


@auth
def user_mod():
    """
    修改用户信息
    :return:
    """
    pass


@auth
def user_del():
    """
    删除用户
    :return:
    """
    pass


@auth
def query_log():
    """
    查询操作日志
    :return:
    """
    pass


@auth
def __main__():
    while True:
        print("主菜单".center(30, "="))
        print('''
    1. 查询用户
    2. 添加用户
    3. 修改用户信息
    4. 删除用户
    5. 日志查询
    6. 退出
    ''')

        choice = {
            1: user_query,
            2: user_add,
            3: user_mod,
            4: user_del,
            5: query_log,
            6: exit
        }

        op = input("请选择：")
        if op.isdigit():
            if int(op) in choice:
                choice[int(op)]()
                continue
        print("非法输入")


__main__()
