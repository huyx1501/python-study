import os
import socket
import hashlib

# 创建socket对象
server = socket.socket()
# 绑定端口
server.bind(("0.0.0.0", 8888))
# 开始监听
print("等待连接...")
server.listen(5)
while True:
    # 与客户端建立连接
    conn, addr = server.accept()  # 建立连接
    print("与客户端%s在%s端口连接成功" % (addr[0], addr[1]))
    m = hashlib.md5()  # 创建MD5对象
    while True:
        try:
            # 接收客户端指令并进行分割
            receive_data = conn.recv(1024).decode()
            if not receive_data: # 当客户端断开时，Linux下会收到空数据包
                print("客户端已断开连接")
                break
        except ConnectionResetError:  # 当客户端断开时，Windows下会抛出异常
            print("客户端已断开连接")
            break
        cmd = receive_data.split()
        method, file_path = cmd[0], cmd[1]
        if os.path.isfile(file_path) and method == "get":  # 判断文件是否存在
            file_size = os.stat(file_path).st_size  # 获取文件大小信息
            print("读取文件大小：%s" % file_size)
            try:
                if file_size:
                    with open(file_path, "rb")as f:  # 以二进制方式打开文件读取
                        conn.send(str(file_size).encode())  # 发送文件大小给客户端
                        conn.recv(1024)  # 等待客户端回应，避免粘包
                        print("开始发送文件")
                        for line in f:
                            conn.send(line)  # 发送数据
                            m.update(line)  # 计算当前MD5值
                    md5 = m.hexdigest()  # 计算最终MD5值
                    print("文件发送完成，md5值为：%s" % md5)
                    conn.send(md5.encode())  # 发送最终的MD5值给客户端
                else:
                    conn.send("文件为空".encode())
            except PermissionError as e:
                conn.send(str(e).encode())  # 发送错误消息给客户端
        else:
            conn.send("指令错误或文件不存在".encode())
