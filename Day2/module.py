import sys
import os

# 打印环境变量
for path in sys.path:
    print(path,"\n")

print(sys.argv) #打印参数

import os
print(os.system("dir"))  #仅打印返回码
print("==========")
print(os.popen("dir").read())  #popen方法仅返回一个内存地址，用read方法去读取
