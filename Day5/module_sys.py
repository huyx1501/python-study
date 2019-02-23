import sys

# 获取程序的运行参数，第一个参数默认是程序本身
print("argv:", sys.argv)

# 获取当前Python版本
print("version:", sys.version)

# 获取python环境变量Path的内容
print("path:", sys.path)

# 获取系统平台名称
print("platform:", sys.platform)

# 打印内容到标准输出
sys.stdout.write("Stdout message\n")
sys.stdout.flush()  # 立即刷新输出缓存，打印消息

# 从标准输入读取内容
print("stdin.readline".center(20,"="))
val = sys.stdin.readline()[:-1]  # [:-1] 去掉末尾的换行符
print(val)
