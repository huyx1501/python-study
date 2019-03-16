import socket

# 初始化socket对象
client = socket.socket()
# 连接服务器端地址
print("开始连接服务器...")
client.connect(("127.0.0.1", 8888))
print("连接服务器成功")
# 循环发送数据
while True:
    data = input(">>")
    if data == "bye": break  # 输入bye关闭连接
    # 发送数据（Python3中必须是bytes类型）
    if len(data) == 0: continue  # 如果输入为空则不发送
    client.send(data.encode("utf-8"))
    # 接收服务器返回的数据
    data_size = int(client.recv(1024).decode("utf-8"))
    if data_size:
        client.send(b"ACK")
    print("结果长度： %s" % data_size)
    received_size = 0
    result = ""
    while received_size != data_size:
        data = client.recv(1024)
        received_size += len(data)
        result += data.decode("utf-8")
        print("已接收长度： %s" % received_size)
    print(result)

# 关闭连接
client.close()
