#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob
"""
采用多线程的方式从ip138网站查询手机号运营商和归属地信息
"""
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import time
import socket
import os
import sys
import threading
from threading import Lock, BoundedSemaphore

args = sys.argv
if len(args) < 3:
    print("""参数错误：
用法：
    python check_phone.py 线程数 源文件 [加-v输出手机号详细信息]
例：
    python check_phone.py 10 C:\phone.txt
""")
    exit(1)

# 防止反爬虫，构造合理的HTTP请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}


class Phone(object):
    def __init__(self, pool, source, details=False):
        # 打开你要查询的号段文档
        basedir = os.path.dirname(source)
        os.chdir(basedir)
        self.f_source = open(r"phone.txt")
        self.f_dianxin = open("电信.txt", "w", encoding="utf-8")
        self.l_dianxin = Lock()
        self.f_yidong = open("移动.txt", "w", encoding="utf-8")
        self.l_yidong = Lock()
        self.f_liantong = open("联通.txt", "w", encoding="utf-8")
        self.l_liantong = Lock()
        self.f_other = open("其他.txt", "w", encoding="utf-8")
        self.l_other = Lock()
        self.f_error = open("错误.txt", "w", encoding="utf-8")
        self.thread_pool = BoundedSemaphore(int(pool))
        self.details = details

    def query(self, number):
        self.thread_pool.acquire()
        count = 0
        while count < 3:
            try:
                url = 'http://www.ip138.com:8080/search.asp?mobile=' + urllib.parse.quote(number) + '&action=mobile'
                # print(url)
                # 用来抓取网页的html源代码
                html = urllib.request.urlopen(url)
                html.encoding = "gb2312"
                # print(html.read().decode("gb2312"))

                # 用来代替正则式取源码中相应标签中的内容
                soup = BeautifulSoup(html, "lxml")
                res = soup.find('tr', bgcolor="#EFF1F3")
                addr = res.next_sibling.next_sibling.find('td', class_="tdc2").get_text().strip()  # 归属地
                if len(addr) == 0:
                    province = ''
                    city = ''
                else:
                    province = addr.split()[0]
                    if len(addr.split()) == 1:
                        city = addr.split()[0] + '市'
                    else:
                        city = addr.split()[1]
                type1 = res.next_sibling.next_sibling.next_sibling.next_sibling.find('td', class_="tdc2").get_text()
                if "电信" in type1:
                    self.l_dianxin.acquire()
                    if self.details:
                        self.f_dianxin.write("{},{},{},{}".format(province, city, type1, number))
                    else:
                        self.f_dianxin.write(number)
                    self.l_dianxin.release()
                elif "联通" in type1:
                    self.l_liantong.acquire()
                    if self.details:
                        self.f_liantong.write("{},{},{},{}".format(province, city, type1, number))
                    else:
                        self.f_liantong.write(number)
                    self.l_liantong.release()
                elif "移动" in type1:
                    self.l_yidong.acquire()
                    if self.details:
                        self.f_yidong.write("{},{},{},{}".format(province, city, type1, number))
                    else:
                        self.f_yidong.write(number)
                    self.l_yidong.release()
                else:
                    self.l_other.acquire()
                    if self.details:
                        self.f_other.write("{},{},{},{}".format(province, city, type1, number))
                    else:
                        self.f_other.write(number)
                    self.l_other.release()
                # print("search result:", "{},{},{},{}".format(province, city, type1, number))
                html.close()
                self.thread_pool.release()
                break
            except Exception:
                print("Failed! Please wait!")
                count += 1
                time.sleep(15)

    @staticmethod
    def check(phone_num):
        if len(phone_num.strip()) != 11:
            return 1
        if str(phone_num)[:2] not in ("13", "15", "16", "17", "18", "19"):
            return 2
        return 0

    def main(self):
        begin_time = time.time()
        # 先建立一个存储爬虫结果的文件
        # 进入工作目录
        os.chdir("//home//bob//mobile")

        # 设置超时时间
        socket.setdefaulttimeout(30)

        for search_item in self.f_source:
            # print("Processing %s" % search_item)
            if self.check(search_item) == 1:
                self.f_error.write("%s, 长度错误" % search_item)
                continue
            elif self.check(search_item) == 2:
                self.f_error.write("%s, 格式错误" % search_item)
                continue
            else:
                t = threading.Thread(target=self.query, args=(search_item,))
                # self.thread_list.append(t)
                t.start()
        else:
            while threading.active_count() != 1:
                print("等待处理数：", threading.active_count())
                time.sleep(1)
            else:
                print("处理完成, 累计用时 %s 秒" % (time.time() - begin_time))
                self.f_source.close()

    def __del__(self):
        try:
            self.f_source.close()
            self.f_yidong.close()
            self.f_liantong.close()
            self.f_dianxin.close()
            self.f_other.close()
            self.f_error.close()
        except Exception:
            pass


try:
    if args[3] == "-v":
        p1 = Phone(args[1], args[2], True)
        p1.main()
except IndexError:
    p1 = Phone(args[1], args[2])
    p1.main()
