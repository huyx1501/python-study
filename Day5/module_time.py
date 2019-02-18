import time
import datetime

print("time.time".center(20, "="))
print(time.time())  # 当前时间戳(timestamp)

print("time.gmtime".center(20, "="))
print(time.gmtime())  # 当前UTC时间的struct_time格式
print("time.localtime".center(20, "="))  # 当前本地时间的struct_time格式
print(time.localtime())

print("time.asctime".center(20, "="))
print(time.asctime())  # 当前时间的字符串格式
print(time.ctime())  # 当前时间的字符串格式


print("时间格式转换".center(20, "="))
# timestamp转struct_time
x = time.localtime(1111111111)
y = time.gmtime(1111111111)
print(x.tm_year)  # 获取年份
print(x.tm_yday)  # 获取一年中的第几天

# struct_time转timestamp
print(time.mktime(x))

# struct_time转指定格式的字符串时间
str_time = time.strftime("%Y-%m-%d %H:%M:%S", x)
print(str_time)

# 字符串时间转struct_time
print(time.strptime(str_time, "%Y-%m-%d %H:%M:%S"))

# 分别从struct_time和timestamp转换成默认格式的字符串时间
print(time.asctime(x))
print(time.ctime(1111111111))


# datetime模块
print("datetime".center(20, "="))
# datetime类的now方法返回当前时间的datetime格式
print(datetime.datetime.now())
print(datetime.datetime.now()+datetime.timedelta(3))  # 获取三天以后的时间
print(datetime.datetime.now()+datetime.timedelta(-3))  # 获取三天以前的时间
print(datetime.datetime.now()+datetime.timedelta(hours=3))  # 获取三小时以后的时间

# 另外两个常用类date和time
print(datetime.date)
print(datetime.time)
