#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pika
import configparser
import os


class RpcServer(object):
    def __init__(self):
        self.connection = None
        self.channel = None
        self.listen = ""
        self.connect()

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
            self.listen = config_reader["server"]["listen"]
            if r_host and r_port and self.listen:
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
                self.channel.queue_declare(queue=self.listen)
                self.channel.basic_consume(queue=self.listen, on_message_callback=self.get_request, auto_ack=False)
            else:
                exit("配置文件有误")
        except KeyError:
            exit("配置文件有误")
        except Exception as e:
            exit("连接RabbitMQ失败 %s" % e)

    def get_request(self, ch, method, properties, body):
        message = body.decode("utf-8")
        print("开始处理消息 ", message)
        result = self.run_cmd(message)
        # print(result)
        if not result:
            result = "Command ERROR"
        # 发送消息到客户端指定的返回队列
        ch.basic_publish(exchange="",
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                         body=str(result))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("消息处理完成 ", message)

    def start(self):
        self.channel.start()

    @staticmethod
    def run_cmd(cmd):
        return os.popen(cmd).read()


if __name__ == "__main__":
    ssh_server = RpcServer()
    print("开始监听...")
    ssh_server.channel.start_consuming()
    ssh_server.connection.close()
