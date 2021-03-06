## 单线程下的高并发FTP服务器(selectors模块实现)
### 程序说明
一个支持多用户登陆的FTP示例程序，主要功能包括：
1. 用户加密认证
2. 允许同时多用户登录
3. 每个用户有自己的家目录 ，且只能访问自己的家目录
4. 对用户进行磁盘配额，每个用户的可用空间不同
5. 允许用户在ftp server上随意切换目录（cd 命令）
6. 允许用户查看当前目录下文件（ls 命令）
7. 允许上传和下载文件，保证文件一致性（put和get命令）
8. 文件传输过程中显示进度条
9. 上传下载支持文件的断点续传
10. 记录操作日志

### 程序结构
```
client
  |--MyFTPClient.py FTP客户端程序
server
  |--core****
    |--server.py 服务器端主程序
  |--data 用户数据目录，启动时自动创建
  |--logs 日志目录，启动时自动创建
  |--config.yml  主配置文件，YAML格式
  |--startup.py  启动程序
README.md(本文档）
```

### 使用说明
客户端程序：
1. 查看当前目录文件：ls
2. 查看子目录文件： ls foo/bar
3. 切换目录：cd foo/bar
4. 删除目录或文件 rm foo/bar
5. 上传文件：put fileX
6. 下载文件: get fileX
    
服务器程序程序：
1. 修改配置文件config.yml
2. 启动程序

### 流程图
![image](https://github.com/huyx1501/python-study/blob/master/Day10/MyFTP_Paralleled/%E5%8D%95%E7%BA%BF%E7%A8%8B%E5%A4%9A%E5%B9%B6%E5%8F%91FTP%E7%BB%93%E6%9E%84%E5%9B%BE.jpg)
