import tarfile

# tar归档文件和目录
tt = tarfile.open('dest.tar', 'w')
tt.add('src_dir/echo.sh')
tt.add('src_dir/src_dir2')  # 会递归归档子目录和文件
tt.close()

# tar解压
tx = tarfile.open('dest.tar','r')
tx.extractall()  # 解压所有文件,默认当前目录
tx.close()