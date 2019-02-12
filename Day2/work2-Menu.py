# 定义一个嵌套的字典
menu = {
    "广东": {
        "广州": {
            "花都": "50001",
            "越秀": "50002",
            "海珠": "50003",
            "黄埔": "50004"
        },
        "深圳": {
            "宝安": "50101",
            "福田": "50102",
            "南山": "50103",
            "龙华": "50104"
        },
        "东莞": {
            "东城": "50201",
            "南城": "50202",
            "莞城": "50203",
            "万江": "50204"
        }
    },
    "湖南": {
        "长沙": {
            "芙蓉": "60001",
            "天心": "60002",
            "雨花": "60003",
            "岳麓": "60004"
        },
        "衡阳": {
            "石鼓": "60201",
            "蒸湘": "60202",
            "珠晖": "60203"
        },
        "郴州": {
            "北湖": "60101",
            "苏仙": "60102"
        }
    },
    "湖北": {
        "武汉": {
            "青山": "70001",
            "武昌": "70002",
            "汉口": "70003",
            "汉阳": "70004"
        },
        "宜昌": {
            "当阳": "70101",
            "虎亭": "70102",
            "夷陵": "70103"
        },
        "荆州": {
            "洪湖": "70201",
            "松滋": "70202"
        }
    }
}

# 第一层循环开始
while True:
    # 循环打印第一层菜单
    for l1 in menu:
        print(l1)
    # 打印完毕提示输入
    choice_l1 = input(">>>:")
    # 判断输入是否属于菜单中的项目
    if choice_l1 in menu:
        # 如果输入正确，进入第二层循环
        while True:
            # 循环打印第二层菜单
            for l2 in menu[choice_l1]:
                print(l2)
            choice_l2 = input(">>>:")
            # 判断第二层输入是否属于第二层菜单中的仓木
            if choice_l2 in menu[choice_l1]:
                # 开始第三层循环
                while True:
                    # 循环打印第三层菜单
                    for l3 in menu[choice_l1][choice_l2]:
                        print(l3)
                    choice_l3 = input(">>>:")
                    # 判断输入是否是第三层菜单的项目
                    if choice_l3 in menu[choice_l1][choice_l2]:
                        # 输入正确打印第三层菜单Key的值
                        print("Code of", choice_l3, "is:", menu[choice_l1][choice_l2][choice_l3])
                        print("".center(20, "="))
                    # 输入r跳出当前while循环，回到上一层while循环
                    elif choice_l3 == "r":
                        break
                    elif choice_l3 == "q":
                        print("Exiting……")
                        exit(0)
                    else:
                        print("Not in list L3")
                        print("".center(20, "="))
            # 输入r跳出当前while循环，回到上一层while循环
            elif choice_l2 == "r":
                break
            elif choice_l2 == "q":
                print("Exiting……")
                exit(0)
            else:
                print("Not in list L2")
                print("".center(20, "="))
    # 输入q退出程序
    elif choice_l1 == "q":
        print("Exiting……")
        exit(0)
    else:
        # 其他输入提示错误并继续当前循环
        print("Not in list L1")
        print("".center(20, "="))
