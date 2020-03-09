#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import traceback

try:
    var = False
    assert var  # 断言不成立时触发AssertionError
except AssertionError:
    traceback.print_exc()  # 打印堆栈信息
