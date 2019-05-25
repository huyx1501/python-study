#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from core.auth import *


@auth
def admin_menu(user):
    member_info = handler.get_member_info(user.member_id, user.role)
    print("欢迎管理员[%s]" % member_info.name)


@auth
def student_menu(user):
    member_info = handler.get_member_info(user.member_id, user.role)
    print("欢迎[%s]同学" % member_info.name)


@auth
def teacher_menu(user):
    member_info = handler.get_member_info(user.member_id, user.role)
    print("欢迎[%s]老师" % member_info.name)


@auth
def main():
    user_type = user_data["user_info"].role
    if user_type == 1:
        admin_menu(user_data["user_info"])
    elif user_type == 2:
        teacher_menu(user_data["user_info"])
    elif user_type == 3:
        student_menu(user_data["user_info"])
    else:
        exit("账户信息异常")


if __name__ == "__main__":
    main()
