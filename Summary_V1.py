# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:09:52 2018
@author: enock
"""

from Model_V1 import *
import numpy as np
import pandas as pd
##分配了多少个任务出去
a = len(x_nonzero)
##多少人被分配了任务
b = []
for i,j in x_nonzero:
    b.append(i)
b = np.unique(b)
b = len(b)
##个人分配数的均值
c = a/i
##个人分配数的方差
d = np.zeros(i)
for i1 in range(0,i):
    for i2,j2 in x_nonzero:
        if i2 == i1+1:
            d[i1] += 1
d = np.var(d)
##个人blockhour的均值
e = np.zeros(i)
for i1 in range(0,i):
    for i2,j2 in x_nonzero:
        if i2 == i1+1:
            e[i1] += BH_j[j2]
e1 = np.mean(e)
##个人blockhour的方差
e2 = np.var(e)
##个人工作日的均值
f = np.zeros(i)
for i1 in range(0,i):
    for i2,j2 in x_nonzero:
        if i2 == i1+1:
            f[i1] += sum(DO_jd[j2][d] for d in range(1,dn))
f1 = np.mean(f)
##个人工作日的方差
f2 = np.var(f)
df = pd.DataFrame({'col1:pairings%':a/n, 'col2:crew%':b/m, 'col3:pair/crew':c, 'col4:var pair/crew':d, 'col5:BH/crew':e1, 'col6:var BH/crew':e2, 'col7:wday/crew':f1, 'col8:var wday/crew':f2},index=['c'])