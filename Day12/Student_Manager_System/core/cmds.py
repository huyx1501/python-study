#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from base_setup import *
from core import db_handler


class Cmds(object):
    def user_query(self, *args):
        return ["user_query", args[0]], 200

    def user_add(self, *args):
        return ["user_add", args[0]], 200

    def user_mod(self, *args):
        return ["user_mod", args[0]], 200

    def user_del(self, *args):
        return ["user_del", args[0]], 200

    def course_query(self, *args):
        return ["course_query", args[0]], 200

    def course_add(self, *args):
        return ["course_add", args[0]], 200

    def course_mod(self, *args):
        return ["course_mod", args[0]], 200

    def course_del(self, *args):
        return ["course_del", args[0]], 200

    def school_query(self, *args):
        return ["school_query", args[0]], 200

    def school_add(self, *args):
        return ["school_add", args[0]], 200

    def school_mod(self, *args):
        return ["school_mod", args[0]], 200

    def school_del(self, *args):
        return ["school_del", args[0]], 200

    def menu_query(self, *args):
        return ["menu_query", args[0]], 200

    def menu_add(self, *args):
        return ["menu_add", args[0]], 200

    def menu_mod(self, *args):
        return ["menu_mod", args[0]], 200

    def menu_del(self, *args):
        return ["menu_del", args[0]], 200

    def auth_query(self, *args):
        return ["auth_query", args[0]], 200

    def auth_add(self, *args):
        return ["auth_add", args[0]], 200

    def auth_mod(self, *args):
        return ["auth_mod", args[0]], 200

    def auth_del(self, *args):
        return ["auth_del", args[0]], 200

    def prov_query(self, *args):
        return ["prov_query", args[0]], 200

    def prov_add(self, *args):
        return ["prov_add", args[0]], 200

    def prov_mod(self, *args):
        return ["prov_mod", args[0]], 200

    def prov_del(self, *args):
        return ["prov_del", args[0]], 200

    def city_query(self, *args):
        return ["city_query", args[0]], 200

    def city_add(self, *args):
        return ["city_add", args[0]], 200

    def city_mod(self, *args):
        return ["city_mod", args[0]], 200

    def city_del(self, *args):
        return ["city_del", args[0]], 200
