import hashlib
import hmac

# 定义一个md5对象
m1 = hashlib.md5()
# 更新对象内容
m1.update("Nice to me you.".encode())
# 打印16进制的md5值
print(m1.hexdigest())
# 追加内容
m1.update("你好".encode(encoding="utf-8"))
print(m1.hexdigest())

# 使用sha256摘要算法
m2 = hashlib.sha256()
m2.update("Nice to me you.你好".encode())
print(m2.hexdigest())

# 使用hma模块加盐计算md5值
m3 = hmac.new("天王盖地虎".encode(), "Nice to me you.你好".encode())
print(m3.hexdigest())