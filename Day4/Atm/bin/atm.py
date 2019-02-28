import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# 导入模块
from main import startup

print("Welcome to ATM")
startup.__main__()
