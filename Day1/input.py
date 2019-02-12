#input 函数：获取用户输入，默认字符串类型
username = input("Input your name:")
#int函数强制转换变量类型
age = int(input("Your age:"))
#print(type(age),type(str(age)))
job = input("Your job:")

# '''XXXX''' 多行字符串
# 用str将age从整型转换成字符串型才能用于拼接
info = '''
Name: ''' + username + '''
age: ''' + str(age) + '''  
job: ''' + job

# %s要求string类型填充，%d要求整型填充，%f要求浮点数填充
info2 = '''
Name: %s
age: %d
job: %s
''' %(username,age,job)

#用format方法执行变量替换
info3 = '''
Name: {_name}
age: {_age}
job: {_job}
'''.format(_name=username,_age=age,_job=job)

#用format方法将变量按顺序填充
info4 = '''
Name: {0}
age: {1}
job: {2}
'''.format(username,age,job)

print(info)

print(info2)

print(info3)

print(info4)