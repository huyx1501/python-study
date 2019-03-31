#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import paramiko


class Controller(object):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def exec(self, cmd):
        shell = paramiko.SSHClient()
        shell.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        shell.connect(hostname=self.host[0], port=self.host[1], username=self.username, password=self.password)
        stdin, stdout, stderr = shell.exec_command(cmd)
        stdout = stdout.read().decode()
        stderr = stderr.read().decode()
        if stdout:
            print('''
[%s - stdout]: 
%s''' % (self.host[0], stdout))
        if stderr:
            print('''
[%s - stderr]: 
%s''' % (self.host[0], stderr))
        shell.close()

    def put(self, src, dest):
        transport = paramiko.Transport(self.host)
        transport.connect(username=self.username, password=self.password)
        scp = paramiko.SFTPClient.from_transport(transport)
        scp.put(src, dest)
        print("文件[%s]上传成功" % src)
        scp.close()
        transport.close()