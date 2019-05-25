#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob
"""
采用多线程的方式从ip138网站查询手机号运营商和归属地信息
"""
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
from urllib.error import URLError
import time
import socket
import sys
import threading
from threading import Lock, BoundedSemaphore
import redis
import traceback

redis_pool = redis.ConnectionPool(host="192.168.2.114", port=6379, decode_responses=True, db=5)  # 创建一个redis连接池
r = redis.Redis(connection_pool=redis_pool)  # 从连接池中申请连接


class Phone(object):
    def __init__(self, phone_num, province, city, type_string, pro_type=4):
        self.phone_num = phone_num
        self.province = province
        self.city = city
        self.type_string = type_string
        self.pro_type = pro_type

    def __repr__(self):
        return {"phone_num": self.phone_num, "province": self.province, "city": self.city,
                "type_string": self.type_string, "pro_type": self.pro_type}


class PhoneCheck(object):
    def __init__(self, pool, source, details=False):
        try:
            # 打开你要查询的号段文档
            self.f_source = open(source)
            self.f_dianxin = open("电信.txt", "w", encoding="utf-8")
            self.l_dianxin = Lock()
            self.f_yidong = open("移动.txt", "w", encoding="utf-8")
            self.l_yidong = Lock()
            self.f_liantong = open("联通.txt", "w", encoding="utf-8")
            self.l_liantong = Lock()
            self.f_other = open("其他.txt", "w", encoding="utf-8")
            self.l_other = Lock()
            self.f_error = open("错误.txt", "w", encoding="utf-8")
            self.l_error = Lock()
        except (FileNotFoundError, IOError, PermissionError) as e:
            exit("打开文件失败 %s" % e)
        self.processed = 0  # 已处理计数器
        self.l_processed = Lock()  # 已处理计数器锁
        self.cached = 0  # 已缓存计数器
        self.l_cached = Lock()  # 已缓存计数器锁
        self.pool = int(pool)
        self.thread_pool = BoundedSemaphore(int(pool))
        # self.l_redis = Lock()
        self.details = details
        self.begin_time = time.time()

    def query(self, number):
        data = r.hgetall(number)
        if data:
            # print(data)
            self.save_data(data)
            self.l_cached.acquire()
            self.cached += 1
            self.l_cached.release()
            if self.pool > 1:
                self.thread_pool.release()
            return
        try:
            url = 'http://www.ip138.com:8080/search.asp?mobile=' + urllib.parse.quote(number) + '&action=mobile'
            # print(url)
            # 用来抓取网页的html源代码
            request = urllib.request.Request(url=url, headers=header)
            html = urllib.request.urlopen(request)
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
            data = Phone(phone_num=number, province=province, city=city, type_string=type1)
            if "电信" in type1:
                data.pro_type = 1
            elif "联通" in type1:
                data.pro_type = 2
            elif "移动" in type1:
                data.pro_type = 3
            else:
                data.pro_type = 4
            # print("search result:", "{}\t{}\t{}\t{}".format(number, province, city, type1))
            self.save_data(data.__repr__())  # 保存数据
            html.close()
            time.sleep(0.1)
            if self.pool > 1:
                self.thread_pool.release()
        except (ConnectionResetError, ConnectionError, URLError) as e:  # 连接异常
            self.l_error.acquire()
            self.f_error.write("%s, 处理超时\n" % number)
            self.l_error.release()
            self.l_processed.acquire()
            self.processed += 1
            self.l_processed.release()
            print("[%s] 处理异常..." % threading.current_thread().name, e)
            try:
                html.close()
            except Exception:
                pass
            time.sleep(10)
            if self.pool > 1:
                self.thread_pool.release()
        except Exception:  # 其他异常
            exit(traceback.format_exc())

    @staticmethod
    def check(phone_num):
        if len(phone_num) != 11:
            return 1
        if str(phone_num)[:2] not in ("13", "14", "15", "16", "17", "18", "19"):
            return 2
        return 0

    def save_data(self, data):
        """
        写入数据到文件
        """
        pro_type = int(data["pro_type"])
        phone_num = data["phone_num"]
        province = data["province"]
        city = data["city"]
        type_string = data["type_string"]
        if pro_type == 1:
            self.l_dianxin.acquire()
            if self.details:
                self.f_dianxin.write("{}\t{}\t{}\t{}\n".format(phone_num, province, city, type_string))
            else:
                self.f_dianxin.write(phone_num+"\n")
            self.l_dianxin.release()
        elif pro_type == 2:
            self.l_liantong.acquire()
            if self.details:
                self.f_liantong.write("{}\t{}\t{}\t{}\n".format(phone_num, province, city, type_string))
            else:
                self.f_liantong.write(phone_num+"\n")
            self.l_liantong.release()
        elif pro_type == 3:
            self.l_yidong.acquire()
            if self.details:
                self.f_yidong.write("{}\t{}\t{}\t{}\n".format(phone_num, province, city, type_string))
            else:
                self.f_yidong.write(phone_num+"\n")
            self.l_yidong.release()
        else:
            self.l_other.acquire()
            if self.details:
                self.f_other.write("{}\t{}\t{}\t{}\n".format(phone_num, province, city, type_string))
            else:
                self.f_other.write(phone_num+"\n")
            self.l_other.release()
        self.l_processed.acquire()
        self.processed += 1
        self.l_processed.release()
        r.hmset(phone_num, data)
        r.expire(phone_num, 3600*24*90)  # 设置键90天后过期删除
        if self.processed > 0 and self.processed % 100 == 0:
            print("已处理 %s 条, 累计用时 %s 秒" % (self.processed, time.time() - self.begin_time))

    def main(self):
        print("开始处理, 请稍候...")
        for search_item in self.f_source:
            # print("Processing %s" % search_item)
            search_item = search_item.strip()
            if search_item == "":
                continue
            if self.check(search_item) == 1:
                self.l_error.acquire()
                self.f_error.write("%s, 长度错误\n" % search_item)
                self.l_error.release()
                continue
            elif self.check(search_item) == 2:
                self.l_error.acquire()
                self.f_error.write("%s, 格式错误\n" % search_item)
                self.l_error.release()
                continue
            else:
                if self.pool > 1:
                    t = threading.Thread(target=self.query, args=(search_item,))
                    self.thread_pool.acquire()
                    # print("处理线程数：", threading.active_count())
                    t.start()
                else:
                    self.query(search_item)
        else:
            while threading.active_count() != 1:
                time.sleep(1)
            else:
                print("""=====处理完成=====
累计处理:  [%d]条
从缓存获取:  [%d]条
累计用时:  %s 秒""" % (self.processed, self.cached, time.time() - self.begin_time))
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


if __name__ == "__main__":
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
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    # 设置超时时间
    socket.setdefaulttimeout(15)

    try:
        if args[3] == "-v":
            p1 = PhoneCheck(args[1], args[2], True)
            p1.main()
    except IndexError:
        p1 = PhoneCheck(args[1], args[2])
        p1.main()

    # p1 = PhoneCheck(5, "/home/bob/Desktop/mobile/phone.txt")
    # p1.main()
