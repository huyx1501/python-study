#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

from greenlet import greenlet


def func1():
    print("From func1")
    gr2.switch()
    print("From func1 again")
    gr2.switch()


def func2():
    print("From func2")
    gr1.switch()
    print("From func2 again")


gr1 = greenlet(func1)
gr2 = greenlet(func2)
gr1.switch()