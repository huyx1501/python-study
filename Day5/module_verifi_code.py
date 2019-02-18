import random

# 初始化变量
code = ""

for i in range(5):
    n = random.randrange(10)
    if n >= 5:
        # 随机返回A-Z的ASCII码并转换成字符
        code_temp = chr(random.randint(65, 90))
    else:
        # 随机返回1-9之间的整数
        code_temp = str(random.randint(1, 9))
    # 循环进行拼接
    code += code_temp

print(code)