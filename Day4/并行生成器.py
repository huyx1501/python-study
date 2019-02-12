import time

# 定义消费者生成器
def consumer(name):
    print("【%s】准备吃包子啦" % name)
    while True:
        baozi = yield
        print("包子【%s】号上桌了，被【%s】吃了一口" % (baozi, name))


def producer():
    # 生成两个消费者并初始化
    c1 = consumer("张三")
    c2 = consumer("李四")
    c1.__next__()
    c2.__next__()
    # 循环制作10个包子
    for i in range(1,10):
        print("包子【%s】号制作完成" % i)
        time.sleep(1)
        # send方法将包子传递给yield作为值
        c1.send(i)
        c2.send(i)


producer()
