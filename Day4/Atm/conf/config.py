import os
import sys

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

database = {
    "db_type": "file",  # 数据库类型，可以是file, mysql等，现在只支持file
    "db_name": "accounts",  # 数据库名，如果是file,则表示数据库所在文件夹
    "db_path": "%s\db" % ROOT,  # 数据库路径, mysql不需要
    "db_user": "",  # 数据库用户名
    "db_pass": ""  # 数据密码
}
