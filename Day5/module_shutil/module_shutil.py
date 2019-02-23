import shutil

# copyfileobj需要将文件操作句柄传递给函数
with open("src_file", "r", encoding="utf-8") as fs, open("dest_file1", "w", encoding="utf-8") as fw1:
    print(type(fs))
    shutil.copyfileobj(fs, fw1, 1000)

# 只需要指定文件名即可完成复制操作
shutil.copyfile("src_file", "dest_file2")

# 拷贝文件权限
shutil.copymode("src_file", "dest_file1")

# 拷贝文件状态信息到一个已存在的文件，包括：mode bits, atime, mtime, flags
shutil.copystat("src_file", "dest_file1")

# 同时拷贝文件内容和文件权限到新文件
shutil.copy("src_file", "dest_file3")

# 同时拷贝文件内容和文件状态到新文件
shutil.copy2("src_file", "dest_file4")

# 递归复制目录到目标（如果目标已存在则报错）
shutil.copytree("src_dir", "dest_dir")
shutil.copytree("src_dir", "dest_dir_del")

# 移动文件或目录
shutil.move("dest_dir", "dest_dir_moved")
shutil.move("dest_file4", "dest_file4_moved")

# 递归删除目录
shutil.rmtree("dest_dir_del")

"""
文件打包和压缩
第一个参数为压缩包存放路径和名字，没路径默认当前目录
第二个参数为打包模式，可以是zip,tar,bztar,gztar
第三个参数为要打包的目录，不填默认当前目录
make_archive实际是调用zipfile和tarfile两个模块进行文件归档压缩
"""
shutil.make_archive("dest_archive", "zip", "src_dir")
