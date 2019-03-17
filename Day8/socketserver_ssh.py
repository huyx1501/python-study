import socketserver
import os


class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                # 接收数据存入变量
                data = self.request.recv(1024)
            except ConnectionResetError:  # 当客户端断开时会抛出异常
                print("Client has gone away...")
                break
            cmd = data.decode("utf-8")  # 解码接收的指令
            cmd_result = os.popen(cmd).read()  # 执行指令
            print("执行指令 %s" % cmd)
            if cmd_result:
                result_size = len(cmd_result.encode("utf-8"))
                self.request.sendall(str(result_size).encode("utf-8"))  # 先发送结果长度
                print("结果长度：%s" % result_size)
                self.request.recv(1024)  # 等待客户端回应，避免粘包
                self.request.sendall(cmd_result.encode("utf-8"))  # 发送命令执行结果
            else:
                self.request.sendall("指令错误".encode())
            print("发送完成")


# 实例化一个socketserver对象
# server = socketserver.TCPServer(("127.0.0.1", 8888), MyHandler)  # 单进程版，一次只能处理一个请求
server = socketserver.ThreadingTCPServer(("127.0.0.1", 8888), MyHandler)  # 多线程版
# server = socketserver.ForkingTCPServer(("127.0.0.1", 8888), MyHandler)  # 多进程版，只能在Linux系统下使用
print("等待连接...")
server.serve_forever()  # 开始监听


