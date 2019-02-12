item_list = {
    "apple": 30,
    "pear": 20,
    "orange": 25,
    "banana": 22,
    "strawberry": 50
}

cart_list = []

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
    for item in item_list:
        print(item, ": $%s" % item_list[item])
    choice = input("Which you want:")
    # 判断输入是否在数组下标范围
    if choice in item_list:
        choice_price = item_list[choice]
        # 从单个商品中获取商品价格并于余额比较
        if balance >= choice_price:
            # 添加商品到购物车列表
            cart_list.append({choice: choice_price})
            # 扣除余额
            balance -= choice_price
            print("Add [%s] to your cart, your balance is [$%s] now" % (choice, balance))
            print("".center(20, "="))
        else:
            print("Not enough money.")
            print("".center(20, "="))
    # 输入字母q退出
    elif choice == "q":
        # center方法在首位填充字符串到指定位数
        print("Your cart item".center(50, "="))
        # 循环打印出购物车列表的所有商品
        for item in cart_list:
            print(item)
        # 打印余额
        print("Left balance : $%s" % balance)
        exit(0)
    else:
        print("item not found.")
        print("".center(20, "="))
