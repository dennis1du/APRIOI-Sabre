# -*- coding: utf-8 -*-

import xlrd
import time
from math import floor, ceil
import pandas as pd
'''
# Size Setting
mt = 9
nt = 672

data_c = pd.read_csv("CrewPrefs.csv", index_col=False)
data_ct = data_c[0:mt]
writer = pd.ExcelWriter("CrewPrefs_test.xlsx")
data_ct.to_excel(writer, index=False)
writer.save()

data_p = pd.read_csv("Pairings.csv", index_col=False)
data_pt = data_p.sample(n=nt, random_state=1)
writer = pd.ExcelWriter("Pairings_test.xlsx")
data_pt = data_pt.sort_index()
data_pt.to_excel(writer, index=False)
writer.save()
'''
'''Data loaded'''
Data_Crew = xlrd.open_workbook("CrewPrefs_all.xlsx")
Data_Pairing = xlrd.open_workbook("Pairings_test.xlsx")

'''Sheets loaded'''
CrewPrefs = Data_Crew.sheet_by_index(0)
Pairings = Data_Pairing.sheet_by_index(0)

'''Pairing data reading'''
# the number of crew memebers/pairings/days/layovers
m = CrewPrefs.nrows - 1
n = Pairings.nrows - 1

# PL_j: the main layover of jth pairing
PL_j = [[]]
for j in range(1, n+1):
    PL_j.append(Pairings.cell_value(j,1))

# PR_j: the Rest End Time of jth pairing (day)
timeArray = time.strptime("2017-04-01 00:00:00", "%Y-%m-%d %H:%M:%S")
timeStamp = int(time.mktime(timeArray))
PR_j = [[]]
for j in range(1,n+1):
    temp = (Pairings.cell_value(j,11))+':00'
    rt = time.strptime((temp), "%m/%d/%Y %H:%M:%S")
    rt_arry = int(time.mktime(rt))
    rt_new = round((rt_arry-timeStamp)/(24*60*60),5)
    rt_new = rt_new + 1
    PR_j.append(rt_new)
# PS_j: the Start Time of jth pairing (day)
PS_j = [[]]
for j in range(1,n+1):
    temp = Pairings.cell_value(j,9)+':00'
    st = time.strptime((temp), "%m/%d/%Y %H:%M:%S")
    st_arry= int(time.mktime(st))
    st_new = round((st_arry-timeStamp)/(24*60*60),5)
    st_new = st_new + 1
    PS_j.append(st_new)
# PE_j: the End Time of jth pairing (day)
PE_j = [[]]
for j in range(1,n+1):
    temp = Pairings.cell_value(j,10)+':00'
    et = time.strptime((temp), "%m/%d/%Y %H:%M:%S")
    et_arry= int(time.mktime(et))
    et_new = round((et_arry-timeStamp)/(24*60*60),5)
    et_new = et_new + 1
    PE_j.append(et_new)

# the number of crew memebers/pairings/days/layovers
dn = floor(max(PE_j[1:]))

# LN_j: the number of legs of jth pairing
LN_j = [[]]
for j in range(1,n+1):
    LN_j.append(int(Pairings.cell_value(j,4)))

# LNMax_j: the max number of legs of jth pairing/duty period
LNMax_j = [[]]
for j in range(1,n+1):
    LNMax_j.append(int(Pairings.cell_value(j,5)))

# LNMax_j: the max number of legs of jth pairing/duty period
LNMin_j = [[]]
for j in range(1,n+1):
    LNMin_j.append(int(Pairings.cell_value(j,6)))

# LD_j: the number of days of jth pairing   
LD_j = [[]]
for j in range(1,n+1):
    LD_j.append(int(Pairings.cell_value(j,3)))

# LH_j: the duty hours of jth pairing
LH_j = [[]]
for j in range(1,n+1):
    LH_j.append(int(Pairings.cell_value(j,7)))

# BH_j: the block hours of jth pairing
BH_j = [[]]
for j in range(1,n+1):
    BH_j.append(int(Pairings.cell_value(j,8)))

# DO_jd: jth pairing has dth day to work/off
DO_jd = [[]]
for j in range(1,n+1):
    row = [0]*dn
    row.insert(0,[])
    for d in range(floor(PS_j[j]), ceil(PE_j[j])):
        row[d] = 1
    DO_jd.append(row)

#O_gh: the gth pairing and the hth pairing are overlapped/not
O_gh = [[]]
for g in range(1,n):
    row = [0]*n
    row.insert(0,[])
    for h in range(g,n+1):
        if not(PR_j[g] < PS_j[h] or PS_j[g] > PR_j[h]):
            row[h] = 1
    O_gh.append(row)

# L_j: If the jth pariing has at least 1 lay-over, L_j = 1; o.w., L_j = 0
L_j = [[]]
for j in range(1,n+1):
    if Pairings.cell_value(j,1) != '-':
        L_j.append(1)
    else:
        L_j.append(0)

'''Prefrence data reading'''
# CP1_i: ith crew member prefers dth for day off 
CP1_i = [[]]
for i in range(1,m+1):
    temp = CrewPrefs.cell_value(i,2)
    if temp != '-' and temp != '':
        do = time.strptime((temp), "%m/%d/%Y")
        do_new = do.tm_mday
    else:
        do_new = -1
    CP1_i.append(do_new)

# CP2_i: ith crew member prefers which lay-over
CP2_i = [[]]
for i in range(1,m+1):
    temp = CrewPrefs.cell_value(i,1)
    if temp != '-' and temp != '':
        CP2_i.append(temp)
    else:
        CP2_i.append(-1)

# CP3Max_i: ith crew member prefers max number of legs/duty period
CP3Max_i = [[]]
for i in range(1,m+1):
    temp = CrewPrefs.cell_value(i,9)
    if temp != '-' and temp != '':
        CP3Max_i.append(int(temp))
    else:
        CP3Max_i.append(-1)
# CP3Min_i: ith crew member prefers min number of legs/duty period
CP3Min_i = [[]]
for i in range(1,m+1):
    temp = CrewPrefs.cell_value(i,8)
    if temp != '-' and temp != '':
        CP3Min_i.append(int(temp))
    else:
        CP3Min_i.append(-1)

# CP4Max_i: ith crew member prefers max pairing length (day)
CP4Max_i = [[]]
for i in range(1,m+1):
    temp = CrewPrefs.cell_value(i,5)
    if temp != '-' and temp != '':
        CP4Max_i.append(int(temp))
    else:
        CP4Max_i.append(-1)
# CP4Min_i: ith crew member prefers min pairing length (day)
CP4Min_i = [[]]
for i in range(1,m+1):
    temp = CrewPrefs.cell_value(i,4)
    if temp != '-' and temp != '':
        CP4Min_i.append(int(temp))
    else:
        CP4Min_i.append(-1)

# CP5Max_i: ith crew member prefers max pairing length (hour)
CP5Max_i = [[]]
for i in range(1,m+1):
    temp = CrewPrefs.cell_value(i,7)
    if temp != '-' and temp != '':
        CP5Max_i.append(int(temp))
    else:
        CP5Max_i.append(-1)
# CP5Min_i: ith crew member prefers min pairing length (hour)
CP5Min_i = [[]]
for i in range(1,m+1):
    temp = CrewPrefs.cell_value(i,6)
    if temp != '-' and temp != '':
        CP5Min_i.append(int(temp))
    else:
        CP5Min_i.append(-1)

# CP6_i: ith crew member prefers min consecutive days off
CP6_i = [[]]
for i in range(1,m+1):
    temp = CrewPrefs.cell_value(i,3)
    if temp != '-' and temp != '':
        CP6_i.append(int(temp))
    else:
        CP6_i.append(-1)