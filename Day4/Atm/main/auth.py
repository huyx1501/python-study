from db import db_controller


def auth(func):
    pass


def lock(data):
    data["status"] = 0
    db_controller.save_info(data)


def login():
    '''
    用户登陆流程
    :return:   认证成功返回用户信息
    '''
    login_count = 0
    while login_count < 3:
        uid = input("ID：")
        info = db_controller.get_info(uid)
        if info:
            if info["status"] == 0:
                print("账户已锁定，请联系管理员")
                return None
            error_count = 0
            while error_count < 3:
                password = input("Password:")
                # 确定密码正确并且账户未锁定
                if password == info["key"] and info["status"] == 1:
                    return info
                elif password == "q":
                    return None
                else:
                    print("密码错误")
                    error_count += 1
            else:
                print("密码错误次数达到三次，锁定账户")
                lock(info)
                return None
        else:
            print("无效ID")
        login_count += 1
    else:
        print("登陆失败次数达到上限")
