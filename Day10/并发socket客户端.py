#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import gevent
import socket

msg_list = [
    "abc",
    "def",
    "123"
]


def connector():
    client = socket.socket()
    client.connect(("127.0.0.1", 8888))
    for msg in msg_list:
        client.send(msg.encode())
        print(client.recv(1024).decode())


gevent.joinall([gevent.spawn(connector) for i in range(1000)])
