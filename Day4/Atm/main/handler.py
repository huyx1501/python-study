from conf import config
from db import db_controller
import re
import calendar


def date_verify(date):
    """
    验证日期的正确性（用异常处理的方法可以很方便识别日期有效性，只是还没学到这块）
    :param date: 输入日期
    :return: 正确返回True，错误返回False
    """
    # 使用正则匹配日期格式
    input_date = re.match("(?P<year>[0-9]{4})-(?P<month>[01][0-9])-(?P<day>[0123][0-9])", date)
    if input_date:
        input_date = input_date.groupdict()
    else:
        return False
    # 判断闰年二月
    if calendar.isleap(int(input_date["year"])):
        if int(input_date["month"]) == 2 and int(input_date["day"]) > 29:
            return False
    else:
        # 判断平年二月
        if int(input_date["month"]) == 2 and int(input_date["day"]) > 28:
            return False
    # 判断其他日期有效性
    if int(input_date["month"]) == 0 or int(input_date["month"]) > 12 \
            or int(input_date["day"]) == 0 or int(input_date["day"]) > 31 \
            or (int(input_date["month"]) in [4, 6, 9, 11] and int(input_date["day"]) > 30):
            return False
    else:
        return True


def query(uid):
    """
    根据ID查询用户信息
    :param uid: 需查询的用户账户
    :return: 返回查询到的用户信息
    """
    return db_controller.get_info(uid)


def query_billing(uid, month):
    """
    根据ID查询用户账单
    :param uid: 需查询账户的用户
    :param month: 要查询的账单月份
    :return: 返回查询到的用户账单
    """
    pass


def query_record(uid, start_time, end_time):
    """
    根据ID查询用户消费明细
    :param uid: 需查询账户的用户
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return: 返回查询到的记录
    """
    pass


def save(data):
    """
    保存用户信息到数据库
    :param data: 需写入的完整用户数据
    :return: None
    """
    return db_controller.save_info(data)


def withdraw(amount, uid):
    """
    用户提现操作
    :param amount: 提现金额，整数
    :param uid: 提现账号
    :return:
        dict：
            flag: 操作结果，布尔值
            fee: 手续费
            balance: 余额
    """
    # 实时查询用户信息
    info = db_controller.get_info(uid)
    # 计算本次提现手续费
    fee = config.transaction["fee"] * amount
    if info:
        # 允许提现额度为账户总额度的50%，剩余额度不足不予提现
        rest_withdraw = info["balance"] - info["credit"] / 2
        if rest_withdraw > amount:
            # 余额计算结果保留两位小数
            balance = round(info["balance"] - amount - fee, 2)
            # 修改账户余额信息
            info["balance"] = balance
            db_controller.save_info(info)
            return {"flag": True, "fee": fee, "balance": balance, "msg": "提现成功"}
        else:
            return {"flag": False, "msg": "可提现额度不足"}
    else:
        return {"flag": False, "msg": "查询账户信息失败"}


def repay(amount, uid):
    """
    用户还款操作
    :param amount: 还款金额，整数
    :param uid: 还款账号
    :return:
        dict：
            flag: 操作结果，布尔值
            balance: 余额
    """
    # 实时查询用户信息
    info = db_controller.get_info(uid)
    if info:
        balance = info["balance"] + amount
        # 修改账户余额信息
        info["balance"] = balance
        db_controller.save_info(info)
        return {"flag": True, "balance": balance, "msg": "还款成功"}
    else:
        return {"flag": False, "msg": "查询账户信息失败"}


def transfer(amount, uid, target):
    """
    用户转账操作
    :param amount: 还款金额，整数
    :param uid: 还款账号
    :param target: 转账目标账户
    :return:
        dict：
            flag: 操作结果，布尔值
            fee: 手续费
            balance: 余额
    """
    # 实时查询用户信息
    target_info = db_controller.get_info(target)
    if not target_info:
        return {"flag": False, "msg": "目标账户不存在"}
    info = db_controller.get_info(uid)
    # 计算本次转账手续费
    fee = config.transaction["trans_fee"] * amount
    if info and target_info:
        balance = info["balance"]
        target_balance = target_info["balance"]
        if balance > amount:
            # 余额计算结果保留两位小数
            balance = round(balance - amount - fee, 2)
            target_balance += amount
            # 修改账户余额信息
            info["balance"] = balance
            target_info["balance"] = target_balance
            db_controller.save_info(info)
            db_controller.save_info(target_info)
            return {"flag": True, "fee": fee, "balance": balance, "msg": "提现成功"}
        else:
            return {"flag": False, "msg": "余额不足"}
    else:
        return {"flag": False, "msg": "查询账户信息失败"}