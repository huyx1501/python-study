import os
import socket
import hashlib

# 创建客户端socket对象
client = socket.socket()
# 连接服务器
client.connect(("127.0.0.1", 8888))
print("连接服务器成功")
while True:
    cmd = input("# ")  # 输入指令
    if len(cmd.split()) != 2:  # 指令应分为两部分，get命令和文件路径
        print("无效指令")
        continue
    client.send(cmd.encode())  # 发送指令到服务器

    file_info = client.recv(1024).decode()  # 接收第一次服务器响应，如果命令和路径正确，应返回文件大小，否则会返回相应错误信息
    if file_info.isdigit():  # 判断返回是否为文件大小
        file_size = int(file_info)
        print("待接收文件大小：%s" % file_size)
        client.send("ACK".encode())  # 发送响应
    else:
        print(file_info)  # 未返回文件大小时直接打印返回的错误消息
        continue

    received_size = 0  # 初始化已接收文件大小
    m = hashlib.md5()  # 创建md5对象，用于对数据进行校验
    print("开始接收文件")
    while received_size < file_size:
        if file_size - received_size > 1024:  # 判断剩余文件大小是否超出1024的缓冲区
            buffer_size = 1024
        else:
            buffer_size = file_size - received_size  # 设置buffer为只接收剩余部分
        save_path = os.path.split(cmd.split()[1])[1]  # 获取输入的文件名，去掉路径
        with open(save_path, "wb") as fw:  # 将要接收的文件暂时放在当前目录下
            data = client.recv(buffer_size)  # 接收数据
            received_size += len(data)  # 累加已接收长度
            # print("已接收长度: %s" % received_size)  # 每次接收打印已接收过的总长度
            m.update(data)  # 计算MD5
            fw.write(data)  # 写入文件
    else:
        print("文件接收完成")
        md5 = m.hexdigest()  # 提取最终的MD5值
        md5_remote = client.recv(1024).decode()  # 获取远程文件的MD5值
        print("原文件MD5: %s  接收文件MD5: %s" % (md5_remote, md5))
