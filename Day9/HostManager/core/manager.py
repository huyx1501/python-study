#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import os
import yaml

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(root_dir, "conf", "config.yml")


def config_parser():
    with open(config_file, "r", encoding="utf-8") as f:
        conf = yaml.load(f, yaml.CLoader if yaml.CLoader else yaml.Loader)
    return conf


def main():
    global config
    config = config_parser()
    print(config)


if __name__ == "__main__":
    main()