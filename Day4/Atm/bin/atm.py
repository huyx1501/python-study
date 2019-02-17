import os
import sys

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, ROOT)

# 导入模块
from main import startup

print("Welcom to ATM")
startup.__main__()
