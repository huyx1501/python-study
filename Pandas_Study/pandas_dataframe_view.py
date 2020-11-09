#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# Author: Bob

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(6, 4), index=list(range(6)), columns=list("ABCD"))

# head方法显示前n行，默认5
print("\n", "DataFrame head()".center(50, "="))
print(df.head(2))

# to_numpy方法转换DataFrame为numpy的array(如果数据类型不同会花费一定计算量)
print("\n", "DataFrame to_numpy()".center(50, "="))
print(df.to_numpy())

# describe方法输出DataFrame的统计信息
print("\n", "DataFrame describe()".center(50, "="))
print(df.describe())

# T属性显示DataFrame行列倒换后的内容T
print("\n", "DataFrame T".center(50, "="))
print(df.T)

# sort_index方法用于对DataFrame进行排序，axis默认为0，即横轴（对行排序），axis=1则为纵轴（对列排序）
# asceding参数默认为True，即升序排序，ascending=False则为降序排序
print("\n", "DataFrame sort_index()".center(50, "="))
print(df.sort_index(axis=0, ascending=False))
print(df.sort_index(axis=1, ascending=False))


# sort_values方法用于对DataFrame按值排序，axis默认为0，即横轴（对行排序），axis=1则为纵轴（对列排序）
# asceding参数默认为True，即升序排序，ascending=False则为降序排序
print("\n", "DataFrame sort_values()".center(50, "="))
print(df.sort_values(by="A", axis=0, ascending=False))  # 按A列的值大小对行排序
print(df.sort_values(by=2, axis=1, ascending=False))  # 按index指定行的值大小对列排序

