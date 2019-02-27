from conf import config
import time
import os

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
    # 如果日志文件夹不存在则创建
    if not os.path.isdir(config.log_conf["log_path"]):
        os.mkdir(config.log_conf["log_path"])
    # 根据配置文件的内容组合出日志文件名
    log_file = "%s%s%s" % (config.log_conf["log_prefix"], date, config.log_conf["log_suffix"])
    # 组合日志文件完整路径
    path = os.path.join(config.log_conf["log_path"], log_file)
    # 打开文件并写入
    with open(path, "a", encoding="utf-8") as log:
        log.write(data)
        log.write("\n")


def log_reader(uid, s_time, e_time):
    """
    读取指定用户的操作日志
    :param uid: 用户id
    :param s_time: 日志开始日期
    :param e_time: 日志结束日期
    :return: 返回查询到的日志信息
    """
    file_list = os.listdir(config.log_conf["log_path"])  # 获取日志目录下的所有文件
    start_time = time.mktime(time.strptime(s_time, "%Y-%m-%d"))  # 输入的开始时间转化为时间戳（这里需要做异常处理，但是还没学...）
    end_time = time.mktime(time.strptime(e_time, "%Y-%m-%d"))  # 输入的结束时间转化为时间戳（这里需要做异常处理，但是还没学...）
    log_lines = []  # 定义一个日志内容的空字典
    for log_file in file_list:  # 遍历日志文件
        filepath = os.path.join(config.log_conf["log_path"], log_file)  # 组合出日志文件的绝对路径
        if os.path.isfile(filepath):  # 判断是否为文件
            log_time = os.path.getctime(filepath)  # 获取文件的创建时间
            if end_time >= log_time >= start_time:  # 确定创建时间在开始和结束时间之间
                with open(filepath, "r", encoding="utf-8") as logf:  # 打开日志文件
                    for log_line in logf:
                        if "[UID=%s]" % uid in log_line:  # 判断UID是否在日志内容中，以确定是该用户的日志条目
                            log_lines.append(log_line)  # 追加当前一行日志到列表中
                        else:
                            continue
        else:
            pass
    return log_lines
