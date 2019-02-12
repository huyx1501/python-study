def out_deco(func_type):
    # 定义高阶函数deco,接收一个函数func作为参数（即函数内存地址）
    def deco(func):
        def wrapper(*args, **kwargs):  # 接收原函数内存地址被替换后传递过来的参数
            if func_type == "N":
                print("Mode N")
            if func_type == "A":
                print("Mode A")
            func(*args, **kwargs)  # 参数重新传递给原函数以保证功能的一致性

        # 返回wrapper函数的内存地址
        return wrapper

    return deco


'''
out_deco(N)函数返回值为deco，@out_deco(N)等同于@deco，即还是以deco作为真正的装饰器（origin1 = deco(origin1)），只是是参数func_type会向下继承;
deco(origin1)执行后返回wrapper，即origin1 = wrapper，那么origin1("参数") = wrapper("参数")，实现最终的装饰；
由于参数_type的继承，可以根据最初指定装饰器时的参数执行不同动作
'''


@out_deco("N")
def origin1(name):
    print("Welcome %s" % name)


@out_deco("A")
def origin2(age):
    print("Age is %s" % age)


# 调用origin1函数实际上等同于调用了wrapper函数，参数name同样也传递给了函数wrapper
origin1("Bob")
origin2(18)