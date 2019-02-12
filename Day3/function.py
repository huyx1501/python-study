
def func1():
    print("Hello")
    return "World"


def func2():
    print("Hello")


print(func1())
print("".center(20,"#"))
print(func2())


def test(x,y,z):
    print(x)
    print(y)
    print(z)


print("".center(20,"#"))
test(1, 2, 3)
print("".center(20,"#"))
test(y=2, x=1, z=3)
print("".center(20,"#"))
test(1, z=3, y=2)


def test_args(name,*args):
    print(name)
    print(args)


print("".center(20,"#"))
test_args("Bob", 18, "Beijing", 90)


def test_kwargs(name,**kwargs):
    print(name)
    print(kwargs)


print("".center(20,"#"))
test_kwargs(name="Bob", age="30", city="Beijing", score="90")
