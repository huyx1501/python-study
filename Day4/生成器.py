
# 列表生成式
x = [ i*2 for i in range(10)]  # i*2可以是其他更复杂的表达式，如将将i传递给函数func(i)
print(x)

# 生成器
y = (i*2 for i in range(10))
print(type(y))
# 生成器每次循环只生成当前需要读取的值放入内存
for i in y:
    print(i)

# 使用__next__方法访问生成器的下一个值
z = (i*2 for i in range(5))
print("Var z".center(20, "="))
print(z.__next__())
print(z.__next__())
print(next(z))
print(next(z))


# 函数式生成器：斐波那契数列函数
def fib(maxnum):
    '''
    表达式a, b = b, a + b实际上相当于
    t = (b, a + b)
    a = t[0]
    b = t[1]
    '''
    n, a, b = 0, 0, 1
    while n < maxnum:
        print(b)
        a, b = b, a + b
        n = n + 1
    return 'Done'


print("Fuction fib".center(20, "="))
fib(10)

print("Generator fib".center(20, "="))
def fib(maxnum):
    n, a, b = 0, 0, 1
    while n < maxnum:
        # yield 将函数变成了一个generator
        yield b
        a, b = b, a + b
        n = n + 1
    # 返回值用于生成器的StopIteration异常时返回值
    return 'Done'


f = fib(10)
print(f)
print(f.__next__())
print(f.__next__())
print(f.__next__())
print(f.__next__())
for i in f:
    print(i)
