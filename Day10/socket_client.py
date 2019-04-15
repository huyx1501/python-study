#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import socket

client = socket.socket()
client.connect(("127.0.0.1", 8888))
while True:
    data = input(">>")
    client.send(data.encode())
    recv = client.recv(1024).decode()
    print(recv)
