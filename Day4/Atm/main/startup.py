import os
import sys

from . import logger
from . import auth
from . import handler


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
def billing_main():
    print("开发中")


# 提现主程序
@auth.auth
def withdraw_main():
    # 提现金额，整数
    amount = input("请输入提现金额：")
    if amount.isdigit():
        # 调用提现操作函数，返回结果保存到变量result
        result = handler.withdraw(int(amount), auth.user_data["user_id"])
        if result["flag"]:
            print("提现成功，提现金额%s，手续费%s，剩余额度%s" % (amount, result["fee"], result["balance"]))
            # 写入日志
            logger.logger()
        else:
            print("提现失败，原因：%s" % result["msg"])
    else:
        print("非法输入")


@auth.auth
def repay_main():
    print("开发中")


@auth.auth
def transfer_main():
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
            2: billing_main,
            3: withdraw_main,
            4: repay_main,
            5: transfer_main,
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
