import json
import os
from conf import config


def file_controller(path, mode, data=None):
    """
    操作文件，读取或写入信息
    :param path:  指定操作文件的路径
    :param mode:  指定读写方式
    :param data:  写模式时要写入的数据
    :return:  读取模式返回读取到的json数据，写模式返回True
    """

    if mode == "w":
        with open(path, "w") as f:
            json.dump(data, f)
            return True
    if mode == "r" and os.path.isfile(path):
        with open(path, "r") as f:
            return json.load(f)


def get_info(uid):
    """
    根据uid查询用户信息
    :param uid:  用户id
    :return:  如果查询到数据返回该用户的信息
    """
    if config.database["db_type"] == "file":
        user_db = "%s.json" % uid
        user_path = os.path.join(config.database["db_path"], config.database["db_name"], user_db)
        return file_controller(user_path, "r")
    if config.database["db_type"] == "mysql":
        pass


def save_info(data):
    """
    将传入的数据保存为json格式的数据
    :param data: json格式数据
    :return: None
    """
    if config.database["db_type"] == "file":
        user_db = "%s.json" % data["id"]
        user_path = os.path.join(config.database["db_path"], config.database["db_name"], user_db)
        return file_controller(user_path, "w", data)

    if config.database["db_type"] == "mysql":
        pass


def remove_user(uid):
    """
    从数据库删除指定用户账户
    :param uid: 要删除的用户ID
    :return: None
    """
    if config.database["db_type"] == "file":
        user_db = "%s.json" % uid
        user_path = os.path.join(config.database["db_path"], config.database["db_name"], user_db)
        if os.path.isfile(user_path):
            os.remove(user_path)

    if config.database["db_type"] == "mysql":
        pass


def list_users():
    """
    从数据库查询当前所有用户
    :return: 返回查询到的用户列表
    """
    file_list = os.listdir(os.path.join(config.database["db_path"], config.database["db_name"]))
    user_list = []
    for file in file_list:
        user_list.append(file.replace(".json", ""))
    return user_list
