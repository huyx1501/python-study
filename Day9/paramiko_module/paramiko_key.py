#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import paramiko

# 创建SSH Key对象
ssh_key = paramiko.RSAKey.from_private_key_file("id_rsa")

# 实例化对象
ssh_client = paramiko.SSHClient()
# 定义密钥策略
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接SSH服务器
ssh_client.connect(hostname="192.168.80.10", port=22, username="root", pkey=ssh_key)

# 执行命令并接收输出
stdin, stdout, stderr = ssh_client.exec_command("free -h && ff")
print(stdout.read().decode())
print("==============================")
print(stderr.read().decode())

# ========================================================================
# 文件传输
# 实例化Transport对象
pipe = paramiko.Transport(("192.168.80.10", 22))  # sock参数可选类型(地址, 端口)，地址:端口，已经实例化的socket对象
# 连接服务器
pipe.connect(username="root", pkey=ssh_key)
# 从Transport示例创建SFTP对象
sftp = paramiko.SFTPClient.from_transport(pipe)
# 上传文件
sftp.put("test_sftp.txt", "/root/test_sftp.txt")
# 下载文件
sftp.get("/root/test_sftp.txt", "test_sftp2.txt")
pipe.close()
