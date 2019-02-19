from conf import config
from db import db_controller


def withdraw(amount, uid):
    '''
    用户提现操作
    :param amount: 提现金额，整数
    :param uid: 提现账号
    :return:
        dict：
            flag: 操作结果，布尔值
            fee: 手续费
            balance: 余额
    '''
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
