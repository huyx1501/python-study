#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import os
import yaml
import threading
import control

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(root_dir, "conf", "config.yml")


def config_parser():
    with open(config_file, "r", encoding="utf-8") as f:
        conf = yaml.load(f, yaml.CLoader if yaml.CLoader else yaml.Loader)
    return conf


def main():
    global config
    config = config_parser()
    groups = config["groups"]
    controller = control.Controller()
    for i, group in enumerate(groups):
        print("%d) - %s 主机数：%d" % (i+1, group["group_name"], len(groups[i]["hosts"])))
    try:
        choice = int(input("请选择主机组："))
        hosts = groups[choice-1]["hosts"]
        for i, host in enumerate(hosts):
            print("\t%d) - %s: %s" % (i + 1, host["hostname"], host["ipaddr"]))
        choice = int(input("请选择主机："))
        cmd = input("sh # ").strip()
        host = hosts[choice-1]
        thread = threading.Thread(target=controller.exec, args=((host["ipaddr"], host["port"]),
                                                                host["username"], host["password"], cmd))
        thread.start()
    except (ValueError, IndexError):
        print("非法输入")


if __name__ == "__main__":
    main()
