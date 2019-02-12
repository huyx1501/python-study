
import time


# 定义装饰器函数，接收参数为被装饰的函数对象
def deco(func):
    # 定义内部函数timer，参数不固定，由func参数中的函数传入
    def timer(*args, **kwargs):
        start_time = time.time()
        # 不固定参数回传给func参数中的函数，并接收其返回值存入临时变量，用于最后返回
        ret = func(*args, **kwargs)
        stop_time = time.time()
        print("Function run time is %s" %(stop_time - start_time))
        return ret
    return timer


@deco  # 定义装饰器，相当于test = deco(test1)，deco(test1)执行结果返回函数timer的内存地址，即test = timer，当调用test("参数") = timer("参数")
def test1():
    time.sleep(1)
    print("Hello")

@deco
def test2(name):
    time.sleep(1)
    return "Welcome %s" % name


test1()
print(test2("Bob"))