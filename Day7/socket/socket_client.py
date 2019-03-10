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
    if data == "bye": break
    # 发送数据（Python3中必须是bytes类型）
    if len(data) == 0: continue
    client.send(data.encode(encoding="utf-8"))
    # 接收服务器返回的数据
    data_back = client.recv(1024).decode(encoding="utf-8")
    print(data_back)

# 关闭连接
client.close()