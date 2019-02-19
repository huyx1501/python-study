import os
import sys

from . import auth
from . import logger


@auth.auth
def query():
    user_info = auth.user_data["user_info"]
    print('''
姓名: %s
额度: ￥%s
可用额度: ￥%s
账单日: %s日
有效期: %s
''' % (user_info["name"], user_info["credit"], user_info["balance"], user_info["pay_day"], user_info["expire_date"]))


@auth.auth
def billing():
    print("开发中")


@auth.auth
def withdraw():
    print("开发中")


@auth.auth
def repay():
    print("开发中")


@auth.auth
def transfer():
    print("开发中")


def logout():
    print("欢迎下次使用，再见")
    exit(0)


@auth.auth
def __main__():
    '''
    启动程序，打印菜单
    '''
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
            2: billing,
            3: withdraw,
            4: repay,
            5: transfer,
            6: logout
        }

        op = input("请选择：")
        if op.isdigit():
            if int(op) in choice:
                choice[int(op)]()
            else:
                print("非法输入")
        else:
            print("非法输入")
