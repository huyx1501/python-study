#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pandas as pd
import numpy as np

# 创建一个Series, np.NaN是numpy中的空值，在Pandas中也有效
s1 = pd.Series([1, 2, np.NaN, 4])
print(s1)
print("Type of s1: %s" % type(s1))

print("".center(50, "="))
# 手工指定index，index可以是数字、字符、日期等类型，并且可重复
s2 = pd.Series([1, 2, np.NaN, 4], index=["a", "b", "c", "d"])
print(s2)

print("".center(50, "="))
# 使用字典创建Series，字典Key即为Series的Index
s3 = pd.Series({
    "a": 1,
    "b": 2,
    "c": "C",
    "d": np.NaN
})
print(s3)

print("".center(50, "="))
# Series的index和values
print(s1.index)
print(s1.values)
print(s3.index)
print(s3.values)
