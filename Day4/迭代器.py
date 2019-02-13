from collections import Iterable
from collections import Iterator

print("Iterable".center(20, "="))
#  可迭代对象
print(isinstance([], Iterable))
print(isinstance({}, Iterable))
print(isinstance(1234, Iterable))
print(isinstance("abcd", Iterable))
print(isinstance((x for x in range(10)), Iterable))

print("Iterator".center(20, "="))
# 迭代器对象
print(isinstance([1, 2, 3, 4], Iterator))
print(isinstance((x for x in range(10)), Iterator))
# iter函数将一个可迭代对象转换成一个迭代器
it = iter([1, 2, 3, 4])
print(isinstance(it, Iterator))
print(next(it))
print(next(it))
print(it.__next__())
