from conf import config
import time

date = time.strftime("%Y-%m-%d", time.localtime())  # 获取当前的年月日，用于日志文件名
datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 获取当前的具体时间，用于日志内容


def logger(uid="", level="INFO", scene="", msg=""):
    """
    日志记录模块
    :param uid: 操作用户的ID
    :param level: 日志级别，默认INFO
    :param scene: 操作场景，如提现，还款等
    :param msg: 具体消息内容
    :return: None
    """
    data = "[%s] [%s] [UID=%s] [%s] - %s" % (datetime, level, uid, scene, msg)
    path = "%s\%s%s%s" \
           % (config.log_conf["log_path"], config.log_conf["log_prefix"], date, config.log_conf["log_suffix"])
    with open(path, "a", encoding="utf-8") as log:
        log.write(data)
        log.write("\n")
