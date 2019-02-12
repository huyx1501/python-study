# 输入用户名
username = input("Username:")

# 打开黑名单文件
with open("./deny.txt", "r", encoding="utf-8") as deny_file:
    # 判断用户名是否在黑名单
    for line in deny_file:
        if line.strip() == username:
            print("You have been blocked!")
            exit(2)

# 初始化计数器
count = 0
# 循环输入密码并进行判断
while True:
    if count < 3:
        # 输入密码
        password = input("Password:")
        with open("./pass.txt", "r", encoding="utf-8") as pass_file:
            for line in pass_file:
                # 判用户名是否匹配
                if username == line.split(":")[0].strip():
                    # 取出对应用户名的密码
                    password_r = line.split(":")[1].strip()
                    # print(password_r)
                    # 判断密码正确性
                    if password_r == password:
                        print("Welcome", username)
                        exit(0)
                    else:
                        # 密码错误重试，计数器+1
                        print("Password error, try again")
                        count += 1
                    break
            else:
                # For循环结束未匹配用户名
                print("User not exist")
                exit(2)
    else:
        # 密码错误三次，写入黑名单
        with open("./deny.txt", "a") as deny_file:
            deny_file.writelines([username, "\n"])
            print("Too many times error, blocked")
            exit(1)
