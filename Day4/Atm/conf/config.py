import os
import sys

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

db_dir = "db"  # 数据库目录相对根目录的路径
log_dir = "logs"  # 日志目录相对根目录的路径


# 数据库配置
database = {
    "db_type": "file",  # 数据库类型，可以是file, mysql等，现在只支持file
    "db_name": "accounts",  # 数据库名，如果是file,则表示数据库所在文件夹
    "db_path": os.path.join(ROOT, db_dir),  # 请勿修改，请修改db_dir配置
    "db_user": "",  # 数据库用户名
    "db_pass": ""  # 数据密码
}

# 交易相关配置
transaction = {
    "interest": 0.15,  # 利息
    "fee": 0.01,  # 提现手续费
    "trans_fee": 0.001  # 转账手续费
}

# 日志相关配置
log_conf = {
    "log_path": os.path.join(ROOT, log_dir),  # 请勿修改，请修改log_dir配置
    "log_prefix": "ATMLog-",  # 日志文件前缀
    "log_suffix": ".log"  # 日志文件后缀
}