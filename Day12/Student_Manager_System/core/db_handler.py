#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from base_setup import *


class Handler(object):
    def __init__(self):
        self.session = SessionClass()

    def get_user(self, uid=None, name=None):
        if uid:
            return self.session.query(User).filter(User.id == uid).first()
        if name:
            return self.session.query(User).filter(User.username == name).first()

    def get_member_info(self, member_id, role_id):
        if not member_id or not role_id:
            return
        if role_id == 1:  # 管理员
            return self.session.query(SysUser).filter(SysUser.id == member_id).first()
        if role_id == 2:  # 教师
            return self.session.query(Teacher).filter(Teacher.id == member_id).first()
        if role_id == 3:  # 学生
            return self.session.query(Student).filter(Student.id == member_id).first()

    def get_school(self):
        pass

    def get_grade(self):
        pass

    def get_register(self):
        pass

    def get_record(self):
        pass

    def get_score(self):
        pass

    def get_rank(self):
        pass

    def get_teach_log(self):
        pass
