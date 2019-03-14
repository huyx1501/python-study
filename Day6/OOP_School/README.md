## 面向对象编程示例-教务管理系统
### 程序说明
这是一个Python面向对象编程的学习示例，主要功能包括：
1. 学员视图
    1. 报名新课程
    2. 查询已报名的班级信息
2. 讲师视图
    1. 设置班级的上下课状态
    2. 查询所在班级信息
	3. 为班级内的学生打分
3. 管理视图
    1. 初始化数据（如果数据文件不存在）
    2. 聘用讲师
	3. 修改课程信息
	4. 查询班级信息

### 程序结构
```
OOP_School
  |--db
    |--school_data.data 数据文件
  |--admin_view.py 管理视图启动程序
  |--student_view.py 学生视图启动程序
  |--teacher_view.py 教师视图启动程序
  |--OPP_School.py 主程序，定义类的相关信息
  |--db_handler.py 用于数据文件的保存和读取
  |--README.md(本文档）
```

### 对象关系图
![image](https://github.com/huyx1501/python-study/raw/dev/Day6/OOP_School/OPP_School%E5%AF%B9%E8%B1%A1%E5%85%B3%E7%B3%BB%E5%9B%BE.jpg)
