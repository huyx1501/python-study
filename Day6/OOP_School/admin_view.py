import OOP_School


def hire_teacher(school):
    teachers = OOP_School.teacher_list
    free_teachers = []
    if teachers:
        for teacher in teachers:
            if teacher.school:
                continue
            else:
                free_teachers.append(teacher)
        if free_teachers:
            for i, teacher in enumerate(free_teachers):
                print("%s. %s 擅长课程：%s" % (i+1, teacher.name, teacher.course.name))
            try:
                choice = int(input("请选择要聘用的老师："))
                salary = int(input("请输入工资："))
                teacher = free_teachers[choice-1]
                school.hire(teacher, salary)
            except ValueError as e:
                print("非法输入")
            except IndexError as e:
                print("无效的选择")
        else:
            print("没有赋闲的教师可供聘用")
    else:
        print("暂无老师")


def manage_class(school):
    classes = school.classes  # 获取学校所有班级
    if classes:
        for i, cl in enumerate(classes):  # 循环打印出所有班级
            print("%s. %s" % (i + 1, cl.name))
        try:
            choice = int(input("请选择要修改的班级："))
            cl = classes[choice - 1]
            print("当前课程信息如下：")
            print("""课程名称： %s
课程周期： %s课时
课程价格： %s元
讲师： %s
学员人数： %d人
""" % (cl.name, cl.course.period, cl.course.price, cl.teacher.name, len(cl.student)))
            print("""
1. 课程周期
2. 课程价格
""")
            choice = int(input("请选择要修改的项目："))
            if choice == 1:
                period = int(input("请输入新的课程周期："))
                cl.course.period = period
            if choice == 2:
                price = int(input("请输入新的课程价格："))
                cl.course.price = price
        except ValueError as e:
            print("非法输入")
        except IndexError as e:
            print("无效的选择")
    else:
        print("还未开设任何班级")


def query_class(school):
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
    for i, school in enumerate(OOP_School.school_list):
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
            elif choice == 2:
                manage_class(school)
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
