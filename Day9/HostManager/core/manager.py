#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import os
import yaml
import threading
from . import control

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(root_dir, "conf", "config.yml")


def config_parser():
    """
    读取配置文件
    :return: 返回配置文件内容
    """
    with open(config_file, "r", encoding="utf-8") as f:
        conf = yaml.load(f, yaml.CLoader if yaml.CLoader else yaml.Loader)
    return conf


def shell(cmd, hosts):
    """
    解析命令并执行
    :param cmd: 要执行的命令
    :param hosts: 执行命令的目标主机
    :return: None
    """
    thread_list = []
    if cmd.startswith("put"):  # 上传文件
        cmd = cmd.split()
        if len(cmd) < 3:
            print("参数错误")
            return
        src = cmd[1]  # 源文件
        dest = cmd[2]  # 目标文件
        dest_filename = os.path.basename(dest) if os.path.basename(dest) else os.path.basename(src)
        dest_path = os.path.dirname(dest) + "/" + dest_filename
        if not os.path.isabs(src):  # 相对路径
            src_path = os.path.join(os.path.dirname(__file__), src)
        else:
            src_path = src
        if os.path.isfile(src_path):
            for host in hosts:
                controller = control.Controller((host["ipaddr"], int(host["port"])), host["username"],
                                                str(host["password"]))
                thread = threading.Thread(target=controller.put, args=(src_path, dest_path))  # 使用新线程执行上传指令
                thread.start()
                thread_list.append(thread)
        else:
            print("源文件不存在")
            return
    else:  # 执行命令
        for host in hosts:
            controller = control.Controller((host["ipaddr"], int(host["port"])), host["username"],
                                            str(host["password"]))
            thread = threading.Thread(target=controller.exec, args=(cmd,))
            thread.start()
            thread_list.append(thread)
    # 等待所有线程返回
    for thread in thread_list:
        thread.join()


def main():
    """
    主程序，与用户交互
    :return: None
    """
    global config
    config = config_parser()  # 获取配置文件内容
    groups = config["groups"]  # 获取主机组信息
    for i, group in enumerate(groups):
        print("%d) - %s 主机数：%d" % (i+1, group["group_name"], len(groups[i]["hosts"])))
    try:
        choice = int(input("请选择主机组："))
        select_group = groups[choice-1]
        hosts = select_group["hosts"]  # 获取指定组下面所有主机
        for i, host in enumerate(hosts):
            print("\t%d) - %s: %s" % (i + 1, host["hostname"], host["ipaddr"]))
        choice = input("请选择主机编号，直接回车将进入批量模式：")
        while True:
            select_host = []
            if not choice:  # 进入批量操作模式
                select_host = hosts
                cmd = input("%s@%s # " % ("batch", select_group["group_name"])).strip()
            else:
                select_host.append(hosts[int(choice)-1])
                cmd = input("%s@%s # " % (select_host[0]["username"], select_host[0]["ipaddr"])).strip()
            if not cmd:
                continue
            elif cmd == "help":
                print('''===使用帮助===：
1. 直接输入命令在远程主机执行命令
2. 输入put命令上传文件到远程目录
3. 输入bye退出
4. 输入help显示帮助''')
                continue
            elif cmd == "bye":
                print("Bye")
                break
            else:
                shell(cmd, select_host)
    except (ValueError, IndexError):
        print("非法输入")
