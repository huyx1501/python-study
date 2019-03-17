import socket
import os

# 初始化socket对象
server = socket.socket()
# 绑定网络地址和端口
server.bind(("0.0.0.0", 8888))
# 开始监听
server.listen(5)
print("开始监听...")
while True:
    # 接受连接，并保存连接对象和对端地址信息
    conn, client_addr = server.accept()
    print("成功建立连接...", client_addr)
    while True:
        # 接受数据存入变量
        try:
            data = conn.recv(1024)
            if not data:  # 当客户端断开时，Linux下会收到空数据包
                print("Client has gone away...")
                break
        except ConnectionResetError:  # 当客户端断开时，Windows下会抛出异常
            print("Client has gone away...")
            break
        cmd = data.decode("utf-8")  # 解码接收的指令
        cmd_result = os.popen(cmd).read()  # 执行指令
        print("执行指令 %s" % cmd)
        if cmd_result:
            result_size = len(cmd_result.encode("utf-8"))
            conn.send(str(result_size).encode("utf-8"))  # 先发送结果长度
            print("结果长度：%s" % result_size)
            conn.recv(1024)  # 等待客户端回应，避免粘包
            conn.send(cmd_result.encode("utf-8"))  # 发送命令执行结果
        else:
            conn.send("指令错误".encode())
        print("发送完成")
