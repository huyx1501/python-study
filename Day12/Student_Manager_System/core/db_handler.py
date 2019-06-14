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

    def get_member_info(self, member_id):
        if member_id:
            return self.session.query(UserInfo).filter(UserInfo.id == member_id).first()

    def get_menu(self, user_id, group_id, pid):
        if not pid:
            menu = self.session.query(Menu.id, Menu.pid, Menu.code, Menu.name)\
                .filter(Menu.id == UserRole.menu_id)\
                .filter(UserRole.user_id == user_id)\
                .filter(Menu.status == 1)\
                .union(self.session.query(Menu.id, Menu.pid, Menu.code, Menu.name)
                       .filter(Menu.id == GroupRole.menu_id)
                       .filter(GroupRole.group_id == group_id)
                       .filter(Menu.status == 1)) \
                .order_by(Menu.id).all()
        else:
            menu = self.session.query(Menu.id, Menu.pid, Menu.code, Menu.name)\
                .filter(Menu.id == UserRole.menu_id)\
                .filter(UserRole.user_id == user_id)\
                .filter(Menu.status == 1)\
                .filter(Menu.pid == pid)\
                .union(self.session.query(Menu.id, Menu.pid, Menu.code, Menu.name)
                       .filter(Menu.id == GroupRole.menu_id)
                       .filter(GroupRole.group_id == group_id)
                       .filter(Menu.status == 1)
                       .filter(Menu.pid == pid))\
                .order_by(Menu.id).all()
        return menu

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
