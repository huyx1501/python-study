import OOP_School
import db_handler


def init():
    """
    如果数据出现错误或第一次运行程序，需进行初始化的必要对象
    执行此方法会覆盖所有现有数据
    :return: None
    """
    # 初始化课程
    Java = OOP_School.Courses("Java", 15000, 60)
    Go = OOP_School.Courses("Go", 20000, 80)
    Python = OOP_School.Courses("Python", 18000, 60)
    OOP_School.course_list = [Java, Go, Python]

    # 初始化学校
    school1 = OOP_School.Schools("武当派", "武当山")
    school2 = OOP_School.Schools("全真教", "终南山")
    OOP_School.school_list = [school1, school2]

    # 初始化教师
    t1 = OOP_School.Teachers("张三丰", 38, "M", Java)
    t2 = OOP_School.Teachers("李清照", 35, "F", Go)
    t3 = OOP_School.Teachers("王重阳", 45, "M", Python)
    OOP_School.teacher_list = [t1, t2, t3]

    # 初始化学生
    s1 = OOP_School.Students("大雄", 15, "M")
    s2 = OOP_School.Students("胖虎", 17, "M")
    s3 = OOP_School.Students("静香", 14, "F")
    OOP_School.student_list = [s1, s2, s3]

    # 组合数据并保存到文件
    OOP_School.data = {"school_list": OOP_School.school_list, "teacher_list": OOP_School.teacher_list, "student_list": OOP_School.student_list, "course_list": OOP_School.course_list}
    db_handler.save_info(OOP_School.data, "data")


def hire_teacher(school):
    """
    操作指定学校进行教师的选择聘用
    :param school: 要招聘教师的学校
    :return: None
    """
    teachers = OOP_School.teacher_list  # 从教师列表读取教师对象信息
    free_teachers = []  # 未被雇佣的教师列表
    if teachers:
        for teacher in teachers:
            if teacher.school:  # 如果教师已经存在学校信息则忽略
                continue
            else:
                free_teachers.append(teacher)  # 将空闲教师加入列表
        if free_teachers:
            # 打印空闲教师列表中的新教师信息
            for i, teacher in enumerate(free_teachers):
                print("%s. %s 擅长课程：%s" % (i+1, teacher.name, teacher.course.name))
            try:
                choice = int(input("请选择要聘用的老师："))
                salary = int(input("请输入工资："))
                teacher = free_teachers[choice-1]
                school.hire(teacher, salary)  # 雇佣教师
            except ValueError as e:
                print("非法输入")
            except IndexError as e:
                print("无效的选择")
        else:
            print("没有赋闲的教师可供聘用")
    else:
        print("暂无老师")


def manage_class(school):
    """
    对学校的课程（班级）进行管理
    :param school: 指定的学校
    :return: None
    """
    classes = school.classes  # 获取学校所有班级
    if classes:  # 判断学校是否已经建立了班级
        for i, cl in enumerate(classes):  # 循环打印出所有班级
            print("%s. %s" % (i + 1, cl.name))
        try:
            choice = int(input("请选择要修改的班级："))
            cl = classes[choice - 1]
            print("当前课程信息如下：")
            print("""课程名称： %s
课程周期： %s课时
课程价格： %s元
讲师：%s
学员人数： %d人
当前状态： %s
""" % (cl.name, cl.course.period, cl.course.price, cl.teacher.name, len(cl.student), "上课中" if cl.status == 1 else "已下课"))
            print("""
1. 课程周期
2. 课程价格
""")
            choice = int(input("请选择要修改的项目："))
            if choice == 1:
                period = int(input("请输入新的课程周期："))
                cl.course.period = period  # 修改班级中课程的周期
            elif choice == 2:
                price = int(input("请输入新的课程价格："))
                cl.course.price = price  # 修改班级中课程的价格
            else:
                print("无效输入")
        except ValueError as e:
            print("非法输入")
        except IndexError as e:
            print("无效的选择")
    else:
        print("还未开设任何班级")


def query_class(school):
    """
    查询指定学校已开设的班级信息
    :param school: 指定的学校
    :return: None
    """
    classes = school.classes  # 获取学校所有班级
    if classes:
        for i, cl in enumerate(classes):  # 循环打印出所有班级
            print("%s. %s" % (i+1, cl.name))
        try:
            choice = int(input("请选择要查询的班级："))
            cl = classes[choice-1]
            print("当前课程信息如下：")
            print("""课程名称： %s
课程周期： %s课时
课程价格： %s元
讲师： %s
学员人数： %d人
""" % (cl.name, cl.course.period, cl.course.price, cl.teacher.name, len(cl.student)))
        except ValueError as e:
            print("非法输入")
        except IndexError as e:
            print("无效的选择")
    else:
        print("还未开设任何班级")


def main():
    # 判断是否存在基础数据，如果没有，提示进行初始化操作
    if not OOP_School.school_list:
        choice = input("天地混沌，啥都没有，是否要开天辟地?(y/n)")
        if choice == ("y" or "Y"):
            init()  # 初始化（开天辟地！）
        else:
            exit("洗洗睡吧")  # 啥都没有就别玩了
    for i, school in enumerate(OOP_School.school_list):  # 打印学校信息
        print("%d. %s %s" % (i+1, school.addr, school.name))
    try:
        choice = int(input("请选择操作学校："))
        school = OOP_School.school_list[choice-1]
        while True:
            print("请选择操作：")
            print("""1. 聘用教师
2. 管理课程
3. 查询班级信息
4. 退出
    """)
            choice = int(input(">>"))
            if choice == 1:
                hire_teacher(school)
                db_handler.save_info(OOP_School.data, "data")  # 保存信息
            elif choice == 2:
                manage_class(school)
                db_handler.save_info(OOP_School.data, "data")  # 保存信息
            elif choice == 3:
                query_class(school)
            elif choice == 4:
                return
            else:
                print("无效输入")
    except ValueError as e:
        print("非法输入")
    except IndexError as e:
        print("无效的选择")


main()
