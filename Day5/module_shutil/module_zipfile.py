import zipfile

# 以写入方式创建压缩包文件
zz = zipfile.ZipFile("dest.zip", "w")
zz.write("src_dir/echo.sh")
zz.write("src_dir/src_dir2")  # 只会压缩目录本身，不包括其内容
zz.close()

# 以读方式打开压缩包
zx = zipfile.ZipFile("dest.zip", "r")
zx.extract("src_dir/echo.sh")  # 解压指定文件到当前目录
zx.extractall()  # 解压所有文件,默认当前目录
zx.close()