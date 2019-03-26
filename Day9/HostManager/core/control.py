#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import paramiko


class Controller(object):
    def __init__(self):
        self.shell = paramiko.SSHClient()
        self.scp = paramiko.SFTPClient
        self.Transport = paramiko.Transport

    def exec(self, host, username, password, cmd):
        self.shell.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell.connect(hostname=host[0],port=host[1], username=username, password=password)
        stdin, stdout, stderr = self.shell.exec_command(cmd)
        print('''[stdout]: 
%s
[stderr]: 
%s''' % (stdout.read().decode(), stderr.read().decode()))

    def upload(self, host, src, dest):
        pass

    def batch(self, group, cmd):
        pass

    def distribute(self, group, src, dest):
        pass
