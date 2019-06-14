## 基于SQLAlchemy的教学管理系统
### 程序说明
C/S架构的教学管理系统，，主要特点：
1. 数据库操作使用SQLAlchemy
2. 基于多线程，支持多用户并发访问
3. 分角色管理，不同角色登陆后功能不同
4. 授权管理，可以实现对指定用户或角色的功能授权


### 程序结构
```
conf  配置文件目录
  |--config.py  服务器主配置文件
  |--init.py  基本组件初始化
core  核心程序目录
  |--cmds.py  命令解析和执行模块
  |--db_handler.py  数据操作模块
  |--server.py  主程序
logs  日志文件目录
base_setup.py  数据库初始化脚本，初始化完成后生成install.lock文件
client.py  客户端
install.lock  初始化后生成，防止重复初始化
startup.py  服务器端启动入口
README.md(本文档）
```

### 使用说明
服务端程序：
1. 修改配置文件config.py
    ```
    # MySQL连接信息
    mysql_config = {
        "Host": "192.168.2.114",    # MySQL主机地址
        "Port": 3306,               # MySQL服务端口
        "User": "root",             # MySQL登陆用户名
        "Password": "12345678",     # MySQL登陆密码
        "DBName": "smsdb",          # MySQL数据库名
        "Charset": "utf8",          # 数据库字符集
        "Prefix": "sm"              # 表前缀
    }

    # 本地服务监听
    local_server = {
        "bind_ip": "0.0.0.0",       # 服务器监听地址
        "bind_port": 9999,          # 服务器监听端口
        "debug": True               # Debug模式，出错时打印traceback
    }

    ```
2. 启动服务器端startup.py

3. 修改客户端client.py中服务器配置信息
    ```
    server = {
        "host": "127.0.0.1",        # 服务器连接地址
        "port": 9999,               # 服务器监听端口
        "debug": True               # 客户端Debug模式
    }
    ```

### 流程图
未完待续...