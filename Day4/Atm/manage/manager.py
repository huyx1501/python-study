import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from conf import config
from db import db_controller
from main import logger
from main import handler

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
        name = input("Admin username：")
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
    date = time.localtime()
    # 新用户默认设置(应以类的方式来定义更合适，但尚未学到到面向对象)
    user_data = {
        # 用户ID
        "id": None,
        # 默认密码
        "key": "123456",
        # 姓名
        "name": "",
        # 创建时间，取当前时间
        "enroll_date": time.strftime("%Y-%m-%d", date),
        # 账单日，取当前日期
        "pay_day": date.tm_mday,
        # 状态，0为锁定，1为正常
        "status": 1,
        # 过期日，默认一年以后
        "expire_date": "%s-%s-%s" % (date.tm_year+1, date.tm_mon, date.tm_mday),
        # 可用额度
        "balance": 15000,
        # 授信额度
        "credit": 15000,
        # 账单，默认空
        "billing": {}
    }

    while True:
        uid = input("Input User ID:")
        if uid.isdigit() and int(uid) > 0:
            info = db_controller.get_info(uid)
            if info:
                print("用户已存在，请重新输入")
            else:
                user_data["id"] = uid
                password = input("请设置用户密码：")
                user_data["key"] = password if password else "123456"
                user_data["name"] = input("请设置用户姓名：")
                credit = int(input("请设置用户额度："))
                user_data["credit"] = credit if credit and credit > 0 else 15000
                user_data["balance"] = user_data["credit"]
                if db_controller.save_info(user_data):
                    print("创建用户成功，用户ID:[%s], 额度:[%d]" % (user_data["id"], user_data["credit"]))
                    return True
                else:
                    print("信息写入不成功，创建用户失败")
                    return False
        else:
            print("非法输入")


@auth
def user_query():
    """
    查询用户信息
    :return:
    """
    user_list = db_controller.list_users()
    if user_list:
        while True:
            print("用户列表".center(30, "="))
            for i, user in enumerate(user_list):
                print("%d. %s" % (i+1, user))
            op = input("如需查询用户详细信息，请输入用户ID，直接回车返回上一层：")
            if not op:
                break
            elif op in user_list:
                user_info = db_controller.get_info(op)
                print('''
姓名: %s
注册时间: %s
额度: ￥%s
可用额度: ￥%s
账单日: %s日
有效期: %s
''' % (user_info["name"], user_info["enroll_date"], user_info["credit"], user_info["balance"], user_info["pay_day"],user_info["expire_date"]))
            else:
                print("非法输入")
    else:
        print("没有查询到用户")


@auth
def user_mod():
    """
    修改用户信息
    :return:
    """
    # 获取最新的用户列表
    user_list = db_controller.list_users()
    if user_list:
        while True:  # 循环打印用户列表
            print("用户列表".center(30, "="))
            for i, user in enumerate(user_list):
                print("%d. %s" % (i + 1, user))
            op = input("请输入要修改的用户ID，直接回车返回上一层：")
            if op in user_list:
                user_info = db_controller.get_info(op)
                print('''
    1. 姓名: %s
    2. 额度: ￥%s
    3. 账单日: %s日
    4. 有效期: %s
    5. 账户状态： %s
    6. 密码： ******
    ''' % (user_info["name"], user_info["credit"], user_info["pay_day"], user_info["expire_date"], "正常" if user_info["status"] == 1 else "冻结"))
                attr = input("请选择需要修改的用户属性：")
                if attr == "1":
                    name = input("请输入新的姓名：")
                    if name:
                        user_info["name"] = name
                    else:
                        print("无效输入")
                        continue
                elif attr == "2":
                    credit = input("请输入新的额度：")
                    if credit.isdigit():
                        if int(credit) >= 0:
                            user_info["credit"] = credit
                    else:
                        print("无效输入")
                        continue
                elif attr == "3":
                    day = input("请输入新的账单日：")
                    if day.isdigit():
                        if 0 < int(day) <= 31:
                            user_info["pay_day"] = day
                    else:
                        print("无效输入")
                        continue
                elif attr == "4":
                    expire_date = input("请输入新的有效期：")
                    if handler.date_verify(expire_date):
                            user_info["expire_date"] = expire_date
                    else:
                        print("无效输入")
                        continue
                elif attr == "5":
                    sure = input("是否修改用户锁定状态（Y/N）：")
                    if sure == "Y" or sure == "y":
                            # 将用户状态减1后取绝对值，则0变成1，1变成0
                            user_info["status"] = abs(int(user_info["status"])-1)
                            if user_info["status"] == 1:
                                print("账户已解冻")
                            else:
                                print("账户已冻结")
                    else:
                        continue
                elif attr == "6":
                    key = input("请输入新密码：")
                    if key:
                            user_info["key"] = key
                    else:
                        print("无效输入")
                        continue
                else:
                    continue

                # 保存修改后的属性
                if db_controller.save_info(user_info):
                    print("用户信息修改成功")
                else:
                    print("保存用户信息失败")
            elif not op:  # 直接回车返回上一层
                break
            else:  # 用户ID输入错误
                print("非法输入")
    else:  # 根据ID未查询到结果（查询异常）
        print("没有查询到用户")


@auth
def user_del():
    """
    删除用户
    :return:
    """
    uid = input("请输入要删除的用户ID：")
    info = db_controller.get_info(uid)
    if info:
        sure = input('''
ID:[%s]
姓名:[%s]
授信额度：[%s]
可用额度：[%s]
确定删除用户吗(Y/N)？
''' % (uid, info["name"], info["credit"], info["balance"]))
        if sure == "Y":
            db_controller.remove_user(uid)
            print("删除用户[%s]成功" % uid)
    else:
        print("输入有误或用户不存在")


@auth
def query_log():
    """
    查询操作日志
    :return:
    """
    start_time = input("请输入查询起始日期（如：2018-01-01）：")
    end_time = input("请输入查询结束日期（如：2018-01-02）：")
    uid = input("请输入要查询的用户ID，不指定用户ID将查询所有用户日志：")
    if handler.date_verify(start_time) and handler.date_verify(end_time):
        results = logger.log_reader(uid, start_time, end_time)
        if results:
            print("符合条件的操作记录如下".center(30, "="))
            for line in results:
                print(line.strip())
        else:
            print("没有查询到结果。")
    else:
        print("日期格式不正确")


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
