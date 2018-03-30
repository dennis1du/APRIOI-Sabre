# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:09:52 2018

@author: enock
"""

from Model import *
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
df = pd.DataFrame({'col1:% of assigned pairings':a,  'col2:% of assingned people':b,  'col3:mean of assigned pairings per person':c,   'col4:var of assigned pairing per person':d,   'col5:mean of assigned BH per person':e1,   'col6:var of assigned BH per person':e2,   'col7:mean of assigned working day per person':f1,   'col8:var of assigned working day per person':f2},index=['c'])