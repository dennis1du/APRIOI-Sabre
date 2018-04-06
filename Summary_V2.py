# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:09:52 2018
@author: enock
"""

from Model_V2 import *
import numpy as np
import pandas as pd
##the percentage of assigned pairings
a = len(x_nonzero)
##the percentage of assigned crew member
b = []
for i,j in x_nonzero:
    b.append(i)
b = np.unique(b)
b = len(b)
##mean of assigned pairings per person
c = a/i
##var of assigned pairings per person
d = np.zeros(i)
for i1 in range(0,i):
    for i2,j2 in x_nonzero:
        if i2 == i1+1:
            d[i1] += 1
d = np.var(d)
##mean of assigned block hours per person
e = np.zeros(i)
for i1 in range(0,i):
    for i2,j2 in x_nonzero:
        if i2 == i1+1:
            e[i1] += BH_j[j2]
e1 = np.mean(e)
##var of assigned block hours per person
e2 = np.var(e)
##mean of working days per person 
f = np.zeros(i)
for i1 in range(0,i):
    for i2,j2 in y_nonzero:
        if i2 == i1+1:
            f[i1] += 1
f1 = np.mean(f)
##var of working days per person
f2 = np.var(f)
df = pd.DataFrame({'col1:pairings%':a/n, 'col2:crew%':b/m, 'col3:pair/crew':c, 'col4:var pair/crew':d, 'col5:BH/crew':e1, 'col6:var BH/crew':e2, 'col7:wday/crew':f1, 'col8:var wday/crew':f2},index=['c'])