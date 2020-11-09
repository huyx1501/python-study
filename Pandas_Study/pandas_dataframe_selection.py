#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(6, 4), index=pd.date_range("20200301", periods=6), columns=list("ABCD"))

# 选择数据列，一下两种方式等效
print("\n", "DataFrame select column[s]".center(50, "="))
print(df["A"])
print(df.A)
print(df[["A", "C"]])  # 同时选择多列

# 使用[]切片
print("\n", "DataFrame slices with []".center(50, "="))
print(df[1:3])  # 和列表的切片一样
print(df["2020-03-02": "2020-03-03"])  # 也可以直接使用索引的名称切片（包含首尾）
