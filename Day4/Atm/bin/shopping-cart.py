import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from main import interface

item_list = [
    ("apple", 30),
    ("pear", 20),
    ("orange", 25),
    ("banana", 22),
    ("strawberry", 50)
]

cart_list = []
price_total = 0


# 调用interface的结算方法
def order(price):
    if price > 0:
        result = interface.order(price_total)
        if result:
            print("订单结算成功，结算金额：%s" % price)
            cart_list.clear()
            return True
        else:
            print("结算失败")
    else:
        print("订单金额不能为0")
        return False


while True:
    print("商品列表".center(50, "="))
    for i, item in enumerate(item_list):
        print("%s. %s - %s元/公斤" % (i+1, item_list[i][0], item_list[i][1]))
    choice = input("请选择要购买的商品，按c查看购物车，按b结算，按x清空购车:")
    # 判断输入是否在数组下标范围
    if choice.isdigit():
        if 0 < int(choice) <= len(item_list):
            choice = int(choice)
            choice_item = item_list[choice-1][0]
            choice_price = item_list[choice-1][1]
            # 添加商品到购物车列表
            cart_list.append(item_list[choice-1])
            print("成功添加[%s]到购物车 " % choice_item)
        else:
            print("指定商品不存在.")
    elif choice == "c":
        # center方法在首位填充字符串到指定位数
        print("当前购物车".center(50, "="))
        # 循环打印出购物车列表的所有商品
        for item in cart_list:
            price_total += item[1]
            print(item)
        print("购物车待结算总金额 [%s]" % price_total)
        con = input("按b结算，按任意键继续")
        if con == "b":
            if order(price_total):
                price_total = 0
    elif choice == "b":
        for item in cart_list:
            price_total += item[1]
        print("购物车待结算总金额 [%s]" % price_total)
        if order(price_total):
            price_total = 0
    elif choice == "x":
        cart_list.clear()
        print("购物车已清空")
    else:
        exit("输入有误，再见")
