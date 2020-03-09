#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pandas as pd
import numpy as np

print("DateIndex".center(50, "="))
# 使用date_range方法创建一个日期index
dates = pd.date_range("20200301", periods=6)
print(dates)
print("Type of dates: %s" % type(dates))

print("\n", "Index from List".center(50, "="))
my_index = pd.Index(["A", "B", "C", "D", "E"])
print(my_index)
print("Type of my_index: %s" % type(my_index))

print("\n", "DataFrame".center(50, "="))
# 创建一个DataFrame, np.random.randn用于创建一个二维数组(numpy.ndarray)，
# index指定索引，索引可以是列表或者pandas索引对象，数量要与二维数组的y轴一致
# columns指定列名，一个列表，长度与二位数组的x轴一致
df1 = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=["A", "B", "C", "D"])
df2 = pd.DataFrame(np.random.randn(6, 4), index=[1, 2, 3, 4, 5, 6], columns=list("ABCD"))
print(df1)
print(df2)
print("Type of df: %s" % type(df1))

print("\n", "DataFrame from dict".center(50, "="))
# 从字典创建DataFrame，字段的每个Key就是一个column，如果某列的值数量仅有一个，就是进行纵向平铺（重复）
# 如果有列的值数量多于一个，但是少于最大的一列值数量，会报错
df3 = pd.DataFrame({'A': 1.,  # 一个浮点数
                    'B': pd.Timestamp('20190101'),  # pandas时间戳格式datetime64[ns]
                    'C': pd.Series(1, index=list("abcd"), dtype='float32'),  # pandas Series对象，手工指定index，dtype手工指定Series的数据类型
                    'D': np.array([3] * 4, dtype='int32'),  # numpy array(数组)对象，[3] * 4表示连续4个3
                    'E': pd.Categorical(["test", "tain", "test", "train"]),  # 使用pandas Categorical(类别)对象作为值
                    'F': 'foo'})
print(df3)
print(df3.dtypes)

print("\n", "Attributions of DataFrame".center(50, "="))
print("Index of df3: %s " % df3.index)  # 索引
print("Columns of df3: %s " % df3.columns)  # 列
print("Values of df3: %s " % df3.values)  # 值
