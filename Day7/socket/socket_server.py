import socket

# 初始化socket对象
server = socket.socket()
# 绑定网络地址和端口
server.bind(("127.0.0.1", 8888))
# 开始监听
server.listen(5)
print("开始监听...")
while True:
    # 接受连接，并保存连接对象和对端地址信息
    conn, client_addr = server.accept()
    print("成功建立连接...", client_addr)
    while True:
        # 接受数据存入变量
        data = conn.recv(1024)
        if not data:
            print("Client has gone away...")
            break
        else:
            data = data.decode(encoding="utf-8")
        print("接收数据完成： ", data)
        # 处理数据后发回客户端
        conn.send(data.upper().encode(encoding="utf-8"))
