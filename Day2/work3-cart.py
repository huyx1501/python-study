# 定义商品列表
item_list = [("apple", 30), ("pear", 20), ("orange", 25), ("banana", 22), ("strawberry", 50)]
# 定义购物车列表
cart_list = []
# 输入初始余额
balance = input("Define your balance:")
# 判断是否为数字
if balance.isdigit():
    # 转换input的string类型为字符串
    balance = int(balance)
else:
    # 输入非数字直接退出
    print("Input error,exit!")
    exit(1)

while True:
    # 使用enumerate方法遍历商品列表内容和下标，并循环打印
    for index,item in enumerate(item_list):
        print(index,item)
    # 选择商品编号（数组下标）
    choice = input("Which you want:")
    # 判断数字
    if choice.isdigit():
        choice = int(choice)
        # 判断输入是否在数组下标范围
        if 0 <= choice < len(item_list):
            # 根据下标获取选择的对象
            choice_item = item_list[choice]
            # 从单个商品中获取商品价格并于余额比较
            if balance >= choice_item[1]:
                # 添加商品到购物车列表
                cart_list.append(choice_item)
                # 扣除余额
                balance -= choice_item[1]
                print("Add [%s] to your cart, your balance is [%s] now" % (choice_item[0], balance))
                print("".center(20, "="))
            else:
                print("Not enough money.")
                print("".center(20, "="))
        else:
            print("item not found.")
            print("".center(20, "="))
    # 输入字母q退出
    elif choice == "q":
        # center方法在首位填充字符串到指定位数
        print("Your cart item".center(50, "="))
        # 循环打印出购物车列表的所有商品
        for cart_item in cart_list:
            print(cart_item)
        # 打印余额
        print("Left balance:", balance)
        exit(0)
    else:
        print("Input error!")
        print("".center(20, "="))
