import re

from . import logger
from . import auth
from . import handler


@auth.auth
def query_info():
    user_info = handler.query(auth.user_data["user_id"])
    print('''
姓名: %s
注册时间: %s
额度: ￥%s
可用额度: ￥%s
账单日: %s日
有效期: %s
''' % (user_info["name"], user_info["enroll_date"], user_info["credit"], user_info["balance"], user_info["pay_day"], user_info["expire_date"]))


@auth.auth
def query_billing():
    billings = handler.account(auth.user_data["user_id"], auth.user_data["user_info"]["pay_day"])
    if billings:
        print("账单列表".center(30, "="))
        months = sorted(billings)
        for i, m in enumerate(months):
            print("%s. %s" % (i+1, m))
        choice = input("请选择查询时间：")
        if choice.isdigit():
            choice = int(choice)
            if months.__len__() >= choice >= 1:
                print("账单金额：￥", billings[months[choice-1]])
                return
        print("非法输入")


@auth.auth
def query_record():
    start_time = input("请输入查询起始日期（如：2018-01-01）：")
    end_time = input("请输入查询结束日期（如：2018-01-02）：")
    if handler.date_verify(start_time) and handler.date_verify(end_time):
        results = logger.log_reader(auth.user_data["user_id"], start_time, end_time)
        if results:
            print("您的操作记录如下".center(30, "="))
            for line in results:
                print(line.strip())
        else:
            print("没有查询到结果。")
    else:
        print("日期格式不正确")


def query_main():
    while True:
        print("查询".center(30, "="))
        print('''
1. 账户信息查询
2. 账单查询
3. 操作记录查询
4. 返回上层
''')

        op = input("请选择：")
        if op == "1":
            query_info()
        elif op == "2":
            query_billing()
        elif op == "3":
            query_record()
        elif op == "4":
            break
        else:
            print("非法输入")


# 提现主程序
@auth.auth
def withdraw_main():
    # 提现金额，整数
    amount = input("请输入提现金额：")
    if amount.isdigit() and int(amount) > 0:
        # 调用提现操作函数，返回结果保存到变量result
        result = handler.withdraw(int(amount), auth.user_data["user_id"])
        if result["flag"]:
            message = "提现成功，提现金额%s，手续费%s，剩余额度%s" % (amount, result["fee"], result["balance"])
        else:
            message = "提现失败，原因：%s" % result["msg"]
        # 打印消息
        print(message)
        # 写入日志
        logger.logger(auth.user_data["user_id"], "INFO" if result["flag"] else "ERROR", "提现", message)
    else:
        print("非法输入")


# 还款主程序
@auth.auth
def repay_main():
    # 还款金额，整数
    amount = input("请输入还款金额：")
    if amount.isdigit() and int(amount) > 0:
        # 调用提现操作函数，返回结果保存到变量result
        result = handler.repay(int(amount), auth.user_data["user_id"])
        if result["flag"]:
            message = "还款成功，还款金额%s，剩余额度%s" % (amount, result["balance"])
        else:
            message = "还款失败，原因：%s" % result["msg"]
        # 打印消息
        print(message)
        # 写入日志
        logger.logger(auth.user_data["user_id"], "INFO" if result["flag"] else "ERROR", "还款", message)
    else:
        print("非法输入")


# 转账主程序
@auth.auth
def transfer_main():
    # 转账金额，整数
    amount = input("请输入转账金额：")
    target = input("请输入目标账户：")
    if amount.isdigit() and int(amount) > 0:
        # 调用提现操作函数，返回结果保存到变量result
        result = handler.transfer(int(amount), auth.user_data["user_id"], target)
        if result["flag"]:
            message = "转账成功，转出金额%s，接收账户[%s]，剩余额度%s" % (amount, target, result["balance"])
        else:
            message = "转账失败，原因：%s" % result["msg"]
        # 打印消息
        print(message)
        # 写入日志
        logger.logger(auth.user_data["user_id"], "INFO" if result["flag"] else "ERROR", "转账", message)
    else:
        print("非法输入")


def logout():
    print("欢迎下次使用，再见")
    exit(0)


@auth.auth
def __main__():
    """
    启动程序，打印菜单
    """
    # 启动记账程序
    handler.account(auth.user_data["user_id"], auth.user_data["user_info"]["pay_day"])
    #  循环打印菜单
    while True:
        print("主菜单".center(30, "="))
        print('''
1. 信息查询
2. 提现
3. 还款
4. 转账
5. 退出
''')

        choice = {
            1: query_main,
            2: withdraw_main,
            3: repay_main,
            4: transfer_main,
            5: logout
        }

        op = input("请选择：")
        if op.isdigit():
            if int(op) in choice:
                choice[int(op)]()
            else:
                print("非法输入")
        else:
            print("非法输入")
