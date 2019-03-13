import OOP_School
import db_handler


def apply(student):
    """
    学生报名
    :param student: 要报名的学生
    :return: None
    """
    # 循环打印出学校列表中的项目
    for i, school in enumerate(OOP_School.school_list):
        print("%s. %s" % (i + 1, school.name))
    try:
        choice = input("请选择学校：")
        school = OOP_School.school_list[int(choice) - 1]  # 选择学校
        if not school.classes:  # 如果学校的班级属性为空则表示学校还没有开班
            print("该学校暂无课程")
            return
        print(("%s课程表" % school.name).center(50, "="))
        for i, cl in enumerate(school.classes):  # 循环打印出学校的全部班级（课程）
            print("%s. 课程：%s  费用：%s  讲师：%s" % (i + 1, cl.name, cl.course.price, cl.teacher.name))
        choice = input("请选择课程：")
        cl = school.classes[int(choice) - 1]  # 选择课程
        if cl in student.classes:  # 确定是否已经报名过同样的课程
            print("已经报名该课程了")
            return
        else:
            print("请缴费%s元" % cl.course.price)  # 获取课程价格
            tuition = input("请缴费：")
            if int(tuition) == cl.course.price:
                school.registry(student, cl)
            elif int(tuition) > cl.course.price:
                print("土豪，不用交这么多钱")
            else:
                print("学费未缴清，报名失败")
    except ValueError as e:
        print("非法输入")
    except IndexError as e:
        print("选择的项不存在")
    except Exception as e:
        print("注册失败,", e)


def query_class(student):
    """
    查询已报名过的班级信息
    :param student: 需要查询的学生
    :return: None
    """
    classes = student.classes  # 获取学生已经报名过的所有班级
    if classes:
        for i, cl in enumerate(classes):  # 循环打印出所有已报名班级
            print("%s. %s - %s" % (i + 1, cl.name, cl.teacher.name))
        try:
            choice = int(input("请选择要查询的班级："))
            cl = classes[choice-1]
            print("当前课程信息如下：")
            print("""课程名称： %s
课程周期： %s课时
课程价格： %s元
所在学校： %s
讲师： %s
学员人数： %d人""" % (cl.name, cl.course.period, cl.course.price, cl.school.name, cl.teacher.name, len(cl.student)))
            try:
                print("在本班分数： %d分" % student.score[cl])
            except KeyError:
                print("在本班分数： 未打分")
        except ValueError as e:
            print("非法输入")
        except IndexError as e:
            print("无效的选择")
    else:
        print("当前还未报名任何课程")


def main():
    for i, student in enumerate(OOP_School.student_list):  # 从学生列表获取所有存在的学生
        print("%d. %s" % (i+1, student.name))
    try:
        choice = int(input("请选择操作用户："))
        student = OOP_School.student_list[choice-1]
        while True:
            print("请选择操作：")
            print("""1. 报名
2. 查询班级信息
3. 退出
    """)
            choice = int(input(">>"))
            if choice == 1:
                apply(student)
                db_handler.save_info(OOP_School.data, "school_data")  # 保存信息
            elif choice == 2:
                query_class(student)
            elif choice == 3:
                return
            else:
                print("无效输入")
    except ValueError as e:
        print("非法输入")
    except IndexError as e:
        print("无效的选择")


main()
