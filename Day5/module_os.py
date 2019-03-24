import os

# 返回当前目录完整路径
print("getcwd: ", os.getcwd())

# 切换目录，相当于cd命令
os.chdir(r"D:\PycharmProjects")
print("After_chdir: ", os.getcwd())

# curdir属性，当前目录.
print("curdir: ", os.curdir)

# pardir属性，父目录..
print("padir: ", os.pardir)

# 递归创建目录
os.makedirs(r"C:\testa\testb\testc")

# 递归删除目录，遇非空目录则停止删除
os.removedirs(r"C:\testa\testb\testc")

# 创建目录
os.mkdir(r"C:\testa")

# 删除目录
os.rmdir(r"C:\testa")

# 以列表返回指定目录下的文件和子目录
print("listdir: ", os.listdir(r"C:\Users\Public"))

# 删除指定文件，如果文件为空则报错
#os.remove(r"C:\temp\test.txt")

# 重命名文件或目录
#os.rename(r"C:\temp", r"C:\tmp")

# 返回文件或目录信息
print("stat: ", os.stat(r"C:\Users\Public"))

# sep属性,当前系统的路径分隔符
print("sep属性: ", os.sep)

# linesep属性,当前系统的行结尾符
print("linesep: ", os.linesep.encode())

# pathsep属性,当前系统变量PATH所用的分隔符
print("pathsep属性: ", os.pathsep)

# environ属性,当前系统的环境变量(字典)
print("environ: ", os.environ)


print("PATH相关: ".center(30, "="))
# 返回指定路径的绝对路径
print("path.abspath: ", os.path.abspath(__file__))

# 将路径拆分成目录和文件名两部分
print("path.split: ", os.path.split(r"C:\temp\test"))

# 返回路径的目录部分
print("path.dirname: ", os.path.dirname(r"C:\temp\test"))

# 返回路径的文件部分
print("path.basename: ", os.path.basename(r"C:\temp\test"))

# 判断路径是否是绝对路径
print("path.isabs: ", os.path.isabs(r"C:\temp\test"))


# 判断文件或目录是否存在
print("path.exists: ", os.path.exists(r"C:\temp\test"))

# 判断目标是否存在并且是文件
print("path.isfile: ", os.path.isfile(r"C:\Windows"))
print("path.isfile: ", os.path.isfile(r"C:\Windows\notepad.exe"))

# 判断目标是否存在并且是目录
print("path.isdir: ", os.path.isdir(r"C:\Windows"))
print("path.isdir: ", os.path.isdir(r"C:\Windows\notepad.exe"))

# 获取文件或目录的访问时间（时间戳）
print("path.getatime: ", os.path.getatime(r"C:\Windows"))

# 获取文件或目录的修改时间（时间戳）
print("path.getctime: ", os.path.getmtime(r"C:\Windows"))

# 获取文件或目录的创建时间（metadata change time ?）（时间戳）
print("path.getctime: ", os.path.getctime(r"C:\Windows"))

# 路径拼接，丢弃绝对路径前的参数(格式“C:”除外）
print("path.join: ", os.path.join(r"C:\Windows", r"system32", r"notepad.exe"))
print("path.join: ", os.path.join(r"Windows", r"\system32", r"notepad.exe"))  # 丢弃最后一个\前的参数
print("path.join: ", os.path.join(r"C:", r"\system32", r"\notepad.exe"))  # 丢弃最后一个\前的参数,盘符除外
print("path.join: ", os.path.join(r"/C", r"/system32", r"/notepad.exe"))  # 丢弃最后一个/前的参数
print("path.join: ", os.path.join(r"\C", r"\system32", r"\notepad.exe"))  # 丢弃最后一个\前的参数
print("path.join: ", os.path.join(r"Windows", r"C:", r"/notepad.exe"))  # 丢弃最后一个/前的参数,盘符除外
