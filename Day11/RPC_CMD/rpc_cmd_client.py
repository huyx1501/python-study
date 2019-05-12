#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika
import configparser
import uuid
import re
import threading


class RpcClient(object):
    def __init__(self):
        self.connection = None
        self.channel = None
        self.tasks = {}
        self.connect()  # 建立RabbitMQ连接

    def __del__(self):
        self.connection.close()

    def connect(self):
        """
        读取配置文件并根据配置文件创建RabbitMQ连接
        :return: None
        """
        config_reader = configparser.ConfigParser()
        try:
            config_reader.read("rabbitmq.cfg")
            r_host = config_reader["rabbitmq"]["host"]
            r_port = config_reader["rabbitmq"]["port"]
            if r_host and r_port:
                try:
                    r_user = config_reader["rabbitmq"]["user"]
                    r_pass = config_reader["rabbitmq"]["password"]
                    credential = pika.PlainCredentials(r_user, r_pass)
                    self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host=r_host, port=r_port, credentials=credential, socket_timeout=5))
                except KeyError:
                    self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host=r_host, port=r_port, socket_timeout=5))
                self.channel = self.connection.channel()
            else:
                exit("配置文件有误")
        except KeyError:
            exit("配置文件有误")
        except Exception as e:
            exit("连接RabbitMQ失败 %s" % e)

    def get_cmd(self, args):
        """
        分解传入的参数，解析出命令和目标主机
        :param args: 用户输入的命令
        :return: None
        """
        method = args.split()[0]
        if method == "exec":
            try:
                args = re.search('.*\s+-m\s+"(?P<cmd>.*)"\s+-h\s+"(?P<host>.*)"$', args).groupdict()
                cmd = args["cmd"]
                host = args["host"]
                if cmd and host:
                    self.run_cmd(cmd, host)  # 执行命令
                else:
                    self.show_help()
            except AttributeError:
                print("参数有误")
                self.show_help()
        elif method == "query":
            args = args.split()[1:]
            for task_id in args:
                if task_id.isdigit():
                    self.get_result(int(task_id))
                else:
                    print("无效ID[%s]" % task_id)
                    return
        else:
            self.show_help()

    def run_cmd(self, cmd, host):

        """
        将命令发送到MQ队列
        :param cmd: 要执行的命令及参数
        :param host: 要执行命令的目标住居
        :return: None
        """
        hosts = host.split(":")
        for h in hosts:
            if self.check_ip(h):  # 检查目标地址是否是IPv4地址
                print("running cmd [%s] on host %s" % (cmd, str(h)))
                self.channel.queue_declare(queue=h)  # 发送消息的队列
                task_id = len(self.tasks)+1
                self.tasks[task_id] = {
                    "host": h,
                    "uuid": str(uuid.uuid4()),
                    "response": "",
                    "reply_queue": None,
                    "reply_thread": None
                }
                tmp_queue = self.channel.queue_declare(queue="", exclusive=True)
                self.tasks[task_id]["reply_queue"] = tmp_queue.method.queue  # 获取临时队列的名称
                self.channel.basic_consume(queue=self.tasks[task_id]["reply_queue"],
                                           on_message_callback=self.process_result,
                                           auto_ack=False)
                self.channel.basic_publish(exchange="", routing_key=h, properties=pika.BasicProperties(
                                            reply_to=self.tasks[task_id]["reply_queue"],
                                            correlation_id=self.tasks[task_id]["uuid"]), body=str(cmd))
                print("任务 id:[%s] 创建成功" % task_id)
            else:
                continue
        threading.Thread(target=self.channel.start_consuming).start()

    def get_result(self, task_id):
        task = self.tasks.get(task_id)
        if task:
            if self.tasks[task_id]["response"]:
                print(self.tasks[task_id]["response"])
            else:
                print("任务处理中，请稍后重试")
        else:
            print("任务不存在id:[%s]" % task_id)

    def process_result(self, ch, method, properties, body):
        """
        获取队列中的消息内容
        :param ch: 返回消息的通道名
        :param method:
        :param properties: 消息的附加属性
        :param body: 消息体
        :return: None
        """
        reply_uuid = properties.correlation_id
        for task_id in self.tasks:
            if self.tasks[task_id]["uuid"] == reply_uuid:
                self.tasks[task_id]["response"] = body.decode("utf-8")
                ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def show_help():
        """
        打印帮助信息
        :return: None
        """
        print('''用法: 
    >> exec -m COMMAND -h HOST[:HOST]
    >> query TASK_ID [TASK_ID]
示例:
    >> exec -m "df -h" -h "192.168.80.10:192.168.80.20"
    >> query 100 101''')

    @staticmethod
    def check_ip(ipaddr):
        """
        检查IPv4地址是否合法
        :param ipaddr: 要检查的地址字符串
        :return: True or False
        """
        # 切割IP地址为一个列表
        ip_split_list = ipaddr.strip().split('.')
        # 切割后列表必须有4个元素
        if 4 != len(ip_split_list):
            return False
        for i in range(4):
            try:
                # 每个元素必须为数字
                ip_split_list[i] = int(ip_split_list[i])
            except ValueError:
                return False
        for i in range(4):
            # 每个元素值必须在0-255之间
            if not 0 <= ip_split_list[i] <= 255:
                return False
        return True


if __name__ == "__main__":
    shell = RpcClient()
    while True:
        data = input(">> ").strip()
        if data:
            shell.get_cmd(data)
