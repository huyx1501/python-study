import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from main import logger
from main import auth
from main import handler


@auth.auth
def order(price):
    if price > 0:
        result = handler.order(price, auth.user_data["user_id"])
        # 写入日志
        logger.logger(auth.user_data["user_id"], "INFO" if result["flag"] else "ERROR", "结算", result["msg"])
        return result["flag"]
    else:
        return False


