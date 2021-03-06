## ATM练习
### 程序说明
这是一个Python模块化编程的学习示例，全部使用python基础知识和部分标准库实现，主要功能包括：
1. 多用户登录
2. 在线购物结算
3. 账户查询
    1. 基本信息查询
    2. 查询账单
    3. 账户流水查询
4. 账户间转账（需手续费）
5. 提现（需手续费）
6. 还款
7. 管理平台
    1. 添加账户
    2. 查询用户信息
    3. 修改用户信息（姓名，额度，有效期，状态，账单日，密码）
    4. 删除用户
    5. 查询用户操作日志

### 程序结构
```
bin
  |--atm.py ATM主程序
  |--shopping-cart.py 购物商城主程序
conf
  |--config.py 主配置文件
db
  |--accounts 存放用户数据库
      |--1001.json 用户数据文件，以ID为文件名
      |--1002.json
  |--db_controller.py 数据库操作模块
logs-- 日志文件目录，自动产生
main
  |--auth.py 用户认证模块
  |--handler.py 数据处理模块
  |--interface.py 购物商城结算接口
  |--logger.py  日志模块
  |--startup.py  用户交互主程序
manage
  |--manager.py 管理平台主程序
README.md(本文档）
```

### 使用说明
ATM程序：
1. 启动程序
2. 验证登陆
3. 可执行查询、取现、还款、转账等操作
    
购物商城程序：
1. 启动程序
2. 选择购物项目
3. 查看购物车或直接结算
4. 调用ATM程序模块进行验证登陆
5. 验证通过结算
    
管理平台程序：
1. 启动程序
2. 管理员登陆
3. 可执行用户的增删改查和日志查询操作

### 流程图
![image](https://github.com/huyx1501/python-study/raw/master/Day4/Atm/ATM%E6%A6%82%E8%A6%81%E6%B5%81%E7%A8%8B%E5%9B%BE.jpg)
