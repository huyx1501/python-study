#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from gevent import monkey  # 引入monkey补丁，是标准库对gevent友好
import gevent
from urllib import request
import time

monkey.patch_all()


def get_url(url):
    print("开始从[%s]下载资源" % url)
    data = request.urlopen(url).read()
    print("下载资源[%s]完成，总下载大小[%s]" % (url, len(data)))


# 顺序执行
start_time = time.time()
get_url("https://www.163.com")
get_url("https://www.github.com")
get_url("https://docs.ansible.com")
print("顺序执行所用时间[%s]" % (time.time() - start_time))

# gevent协程
start_time = time.time()
gevent.joinall([
    gevent.spawn(get_url, "https://www.163.com"),
    gevent.spawn(get_url, "https://www.github.com"),
    gevent.spawn(get_url, "https://docs.ansible.com"),
])
print("协程执行所用时间[%s]" % (time.time() - start_time))