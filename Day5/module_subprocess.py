#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import subprocess
import sys
import signal

print("subprocess.PIPE".center(50, "#"))
# 通过subprocess.PIPE接收命令返回
if sys.platform == "win32":
    # 以元组形式传递要执行的命令和命令的参数
    a = subprocess.run(["ipconfig", "/all"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
else:
    a = subprocess.run(["ip", "a"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(a.stdout)

print("check=True".center(50, "#"))
# check=True时，如果命令返回值不是0，触发subprocess.CalledProcessError
try:
    if sys.platform == "win32":
        a = subprocess.run(["ipconfig", "123"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    else:
        a = subprocess.run(["ip", "123"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(a.stdout)
except subprocess.CalledProcessError as e:
    print(e)
    print("")

print("shell=True".center(50, "#"))
# 当shell=True时，参数中的命令部分写为字符串，整个提交给命令行执行，一般用于命令中有管道的情况
if sys.platform == "win32":
    a = subprocess.run('ipconfig /all | find "192.168"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
else:
    a = subprocess.run("ip a | grep '192.168'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
print(a.stdout)

print("call()".center(50, "#"))
# subprocess的call方法将结果输出到标准输出，并返回一个状态码
if sys.platform == "win32":
    a = subprocess.call(['ipconfig'])
    print(a)
else:
    a = subprocess.run(["ip"])
    print(a)

print("check_call()".center(50, "#"))
# check_call方法与call方法不同点在于当返回值不为0时抛出异常
try:
    a = subprocess.check_call('["bbb"]')
    print(a)
except Exception as e:
    print(e)
    print("")

print("getoutput()".center(50, "#"))
if sys.platform == "win32":
    a = subprocess.getoutput("ipconfig")
    print(a)
else:
    a = subprocess.getoutput("ip")
print("")

print("getstatusoutput()".center(50, "#"))
# getstatusoutput方法返回一个命令返回码和结果组成的元祖
if sys.platform == "win32":
    a = subprocess.getstatusoutput("ipconfig")
    print(a)
else:
    a = subprocess.getstatusoutput("ip")
print("")

print("check_output()".center(50, "#"))
# check_output当命令返回值非0时抛出异常，否则返回命令结果
try:
    a = subprocess.check_call('["ls"]')
    print(a)
except Exception as e:
    print(e)
    print("")

print("subprocess.Popen".center(50, "#"))
# Popen方法执行后立即返回一个subprocess.Popen对象，不等待结果
if sys.platform == "win32":
    # 以元组形式传递要执行的命令和命令的参数
    a = subprocess.Popen(["ipconfig", "/all"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(a.stdout.read())
else:
    a = subprocess.Popen(["ip", "a"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(a.stdout.read())

if sys.platform == "linux":
    a = subprocess.Popen("for (( i=0; i<100; i++)); do echo $i; sleep 1; done", stdout=subprocess.PIPE, shell=True)
    print(type(a))
    a.terminate()  # 结束进程，相当于kill命令
    a.send_signal(signal.SIGTERM)  # 向程序发送信号，SIGTERM相当于terminate方法
    a.kill()  # 强制结束进程，相当于kill -9 命令


