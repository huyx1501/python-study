## 基于RabbitMQ的远程SHELL
### 程序说明
通过RabbitMQ实现模拟RPC调用在多目标主机上执行命令，异步返回命令执行结果：
1. 所有通信基于RabbitMQ
2. 批量执行或单独执行
3. 跨平台支持
4. 异步的结果显示


### 程序结构
```
RPC_CMD
  |--rabbitmq.cfg  主配置文件
  |--rpc_cmd_client.py  RPC客户端（控制端）
  |--rpc_cmd_server.py  RPC服务端（被控端）
README.md(本文档）
```

### 使用说明
服务端程序：
1. 修改配置文件rabbitmq.cfg
    ```
    # RabbitMQ服务器信息
    [rabbitmq]
    host = 192.168.2.114  # 服务器地址
    port = 5672  # 服务器端口
    user = guest  # RabbitMQ用户名
    password = guest  # RabbitMQ密码
    
    [server]
    listen = 192.168.80.10  # 服务器端监听地址（监听队列名称）
    ```
2. 启动rpc_cmd_server.py

客户端程序：
1. 修改配置文件rabbitmq.cfg
2. 启动rpc_cmd_client.py
3. 指令说明
    ```
    >> exec -m "COMMAND" -h "HOST[:HOST]"  # 执行任务
    >> query TASK_ID [TASK_ID]  # 查询指定任务
    >> list  # 显示任务列表及状态
    ```

### 流程图
待补充
