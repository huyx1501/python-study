import time
from . import handler

# 用户临时变量，存储用户验证信息
user_data = {
    "user_id": "",
    "is_login": False,
    "user_info": {}
}


def lock(uid):
    """
    锁定用户
    :param uid: 需要锁定用户账户
    :return: None
    """
    info = handler.query(uid)
    info["status"] = 0
    handler.save(info)


def login():
    """
    用户登陆流程
    :return:   认证成功返回用户信息
    """
    login_count = 0
    while login_count < 3:
        uid = input("ID：")
        info = handler.query(uid)
        if info:
            if info["status"] == 0:
                print("账户已锁定，请联系管理员")
                return False
            e_date = time.mktime(time.strptime(info["expire_date"], "%Y-%m-%d"))
            if e_date < time.time():
                print("账户已过期，请联系管理员")
                return False
            error_count = 0
            while error_count < 3:
                password = input("Password:")
                # 确定密码正确并且账户未锁定
                if password == info["key"] and info["status"] == 1:
                    # 账户密码匹配，修改用户临时变量
                    user_data["user_id"] = info["id"]
                    user_data["is_login"] = True
                    user_data["user_info"] = info
                    return True
                elif password == "q":
                    return False
                else:
                    print("密码错误")
                    error_count += 1
            else:
                print("密码错误次数达到三次，锁定账户")
                lock(uid)
                return False
        else:
            print("无效ID")
        login_count += 1
    else:
        print("登陆失败次数达到上限")


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
            else:
                exit(1)
    return wrapper

