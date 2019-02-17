import json
import os
from conf import config


def file_controller(path, mode, data=None):
    '''
    操作文件，读取或写入信息
    :param path:  指定操作文件的路径
    :param mode:  指定读写方式
    :param data:  写模式时要写入的数据
    :return:  读取模式返回读取到的json数据，写模式返回None
    '''
    if os.path.isfile(path):
        if mode == "w":
            with open(path, "w") as f:
                json.dump(data, f)
        if mode == "r":
            with open(path, "r") as f:
                return json.load(f)


def get_info(uid):
    '''
    根据uid查询用户信息
    :param uid:  用户id
    :return:  如果查询到数据返回该用户的信息
    '''
    if config.database["db_type"] == "file":
        user_path = "%s\%s\%s.json" % (config.database["db_path"], config.database["db_name"], uid)
        return file_controller(user_path, "r")
    if config.database["db_type"] == "mysql":
        pass


def save_info(data):
    '''
    将传入的数据保存为json格式的数据
    :param data: json格式数据
    :return: None
    '''
    if config.database["db_type"] == "file":
        user_path = "%s\%s\%s.json" % (config.database["db_path"], config.database["db_name"], data["id"])
        file_controller(user_path, "w", data)

    if config.database["db_type"] == "mysql":
        pass
