import os
import sys

from . import auth
from . import logger


user_data = {
    "user_id": "",
    "is_login": False,
    "user_info": {}
}


def query():
    user_info = user_data["user_info"]
    print('''
姓名: %s
额度: ￥%s
可用额度: ￥%s
账单日: %s日
有效期: %s
''' % (user_info["name"], user_info["credit"], user_info["balance"], user_info["pay_day"], user_info["expire_date"]))


def withdraw():
    print("开发中")


def repay():
    print("开发中")


def transfer():
    print("开发中")


def logout():
    print("欢迎下次使用，再见")
    exit(0)


def __main__():
    '''
    启动程序，用户登陆
    '''
    # 登陆成功，保存用户登陆
    login = auth.login()
    if login:
        user_data["user_id"] = login["id"]
        user_data["is_login"] = True
        user_data["user_info"] = login
    else:
        exit(1)

    #  循环打印菜单
    while True:
        print('''
========Menu========
1. 账户信息查询
2. 账单查询
3. 提现
4. 还款
5. 转账
6. 退出
'''
              )

        choice = {
            1: query,
            2: withdraw,
            3: repay,
            4: transfer,
            5: logout
        }

        op = input("请选择：")
        if op.isdigit():
            choice[int(op)]()
        else:
            print("非法输入")
