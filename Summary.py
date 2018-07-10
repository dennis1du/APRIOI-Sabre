# -*- coding: utf-8 -*-

from Model import *
import numpy as np
import pandas as pd

'''Percentage of Assigned Pairings'''
a = len(x_nonzero)
p1 = a/n

'''Percentage of Assigned Crew Member'''
b = []
for i,j in x_nonzero:
    b.append(i)
b = np.unique(b)
b = len(b)
p2 = b/m

'''Average Assigned Pairings per Crew Member'''
c = a/i

'''Variance of Assigned Pairings per Crew Member'''
d = np.zeros(i)
for i1 in range(0,i):
    for i2,j2 in x_nonzero:
        if i2 == i1+1:
            d[i1] += 1
d = np.var(d)

'''Average Assigned Block Hours per Crew Member'''
e = np.zeros(i)
for i1 in range(0,i):
    for i2,j2 in x_nonzero:
        if i2 == i1+1:
            e[i1] += BH_j[j2]
e1 = np.mean(e)

'''Variance of Assigned Block Hours per Crew Member'''
e2 = np.var(e)

'''Average Working Days per Crew Member'''
f = np.zeros(i)
for i1 in range(0,i):
    for i2,j2 in y_nonzero:
        if i2 == i1+1:
            f[i1] += 1
f1 = np.mean(f)

'''Variance of working days per Crew Member'''
f2 = np.var(f)

'''Summary'''
df = pd.DataFrame({'col1:pairings%':p1, 'col2:crew%':p2, 'col3:pair/crew':c, 'col4:var pair/crew':d, 'col5:BH/crew':e1, 'col6:var BH/crew':e2, 'col7:wday/crew':f1, 'col8:var wday/crew':f2},index=['c'])