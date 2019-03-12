import OOP_School
import db_handler


def start_class(teacher):
    return teacher.start_class()  # 调用类的上课方法


def finish_class(teacher):
    return teacher.finish_class()  # 调用类的下课方法


def query_class(teacher):
    """
   查询教师所在的班级信息
    :param school: 指定的教师
    :return: None
    """
    cl = teacher.classes  # 获取教师所教的班级
    print("当前课程信息如下：")
    print("""课程名称： %s
课程周期： %s课时
课程价格： %s元
所在学校： %s
学员人数： %d人
""" % (cl.name, cl.course.period, cl.course.price, cl.school.name, len(cl.student)))


def score(teacher):
    students = teacher.classes.student  # 获取班级里面所有学生的列表
    if students:
        for i, student in enumerate(students):  # 循环打印出所有学生
            print("%s. %s" % (i+1, student.name))
        try:
            choice = int(input("请选择学生："))
            selected = students[choice-1]
            scores = int(input("请打分："))
            selected.score[teacher.classes] = scores  # 将分数赋予所选学生的当前课程（即学生在本班的分数）
        except ValueError as e:
            print("非法输入")
        except IndexError as e:
            print("选择的项不存在")
    else:
        print("当前课程暂无学生")


def main():
    # 展示所有教师信息
    for i, teacher in enumerate(OOP_School.teacher_list):
        print("%d. %s %s" % (i+1, teacher.school.name if teacher.school else "游侠", teacher.name))
    try:
        choice = int(input("请选择操作用户："))
        teacher = OOP_School.teacher_list[choice-1]
        while True:
            print("请选择操作：")
            print("""1. 上课
2. 下课
3. 查询班级信息
4. 为学生打分
5. 退出
    """)
            choice = int(input(">>"))
            if choice == 1:
                if not teacher.school:  # 如果教师属性school未空则表示还没有被学校雇佣，不允许进行相关操作
                    print("您还未被学校雇佣")
                    continue
                start_class(teacher)  # 调用上课方法
                db_handler.save_info(OOP_School.school_list, "school_list")  # 保存学校信息
            elif choice == 2:
                if not teacher.school:
                    print("您还未被学校雇佣")
                    continue
                finish_class(teacher)  # 调用下课方法
                db_handler.save_info(OOP_School.school_list, "school_list")  # 保存学校信息
            elif choice == 3:
                if not teacher.school:
                    print("您还未被学校雇佣")
                    continue
                query_class(teacher)
            elif choice == 4:
                if not teacher.school:
                    print("您还未被学校雇佣")
                    continue
                score(teacher)
                db_handler.save_info(OOP_School.student_list, "student_ist")  # 保存学生信息
            elif choice == 5:
                return
            else:
                print("无效输入")
    except ValueError as e:
        print("非法输入")
    except IndexError as e:
        print("无效的选择")


main()
