import os
import sys

# 获取程序根目录
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 加入环境变量
sys.path.append(root_path)

# 导入模块
from conf import config
from main import main

print("Welcom to ATM")
main.__main__()
