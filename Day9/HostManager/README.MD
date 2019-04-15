## 主机远程管理练习
### 程序说明
1. 使用paramiko模块远程管理主机
2. 支持批量管理，使用多线程
3. 支持远程执行shell命令和文件上传

### 程序结构
```
conf
  |--config.yml  主配置文件，YAML格式
core
  |--control.py  Controller类使用paramiko模块执行远程命令
  |--manager.py  主程序，用于交互和命令解析
startup.py  启动程序
README.md(本文档）
```

### 使用说明
1. 启动程序显示主机分组信息
2. 选择分组后显示组内的主机列表
3. 选择主机或直接进入批量模式，得到一个本地shell
    1. 直接输入命令在远程主机执行命令
    2. 输入put命令上传文件到远程目录
    3. 输入bye退出程序

### 流程图
![image](https://raw.githubusercontent.com/huyx1501/python-study/master/Day9/HostManager/%E4%B8%BB%E6%9C%BA%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%E5%9F%BA%E6%9C%AC%E6%B5%81%E7%A8%8B%E5%9B%BE.jpg)
