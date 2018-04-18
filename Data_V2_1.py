# -*- coding: utf-8 -*-

import xlrd
import time
from datetime import datetime
from xlrd import xldate_as_tuple
from math import floor, ceil
import pandas as pd

# Size Setting
m = 5
nt = 100
data = pd.read_csv("Pairings.csv", index_col=False)
data1 = data.sample(n=nt, random_state=1)
writer = pd.ExcelWriter('test.xlsx')
data1.to_excel(writer, index=False)
writer.save()

'''Data loaded'''
Data_File = xlrd.open_workbook("test.xlsx")

'''Sheets loaded'''
Main_Sheet = Data_File.sheet_by_index(0)
#Overlap = Data_File.sheet_by_index(1)
#Day_Off = Data_File.sheet_by_index(2)
#Pairing_Layover = Data_File.sheet_by_index(3)
#CP1 = Data_File.sheet_by_index(5)
#CP2 = Data_File.sheet_by_index(6)

'''global data reading'''
# the number of crew memebers/pairings/days/layovers
n = Main_Sheet.nrows - 1

# PR_j: the Rest End Time of jth pairing (day)
PR_j = [[]]
for j in range(1,n+1):
    temp = Main_Sheet.cell_value(j,11)+':00'
    rt = time.strptime((temp), "%m/%d/%Y %H:%M:%S")
    rt_new = round(rt.tm_mday+rt.tm_hour/24+rt.tm_min/(60*24),5)
    PR_j.append(rt_new)
# PS_j: the Start Time of jth pairing (day)
PS_j = [[]]
for j in range(1,n+1):
    temp = Main_Sheet.cell_value(j,9)+':00'
    st = time.strptime((temp), "%m/%d/%Y %H:%M:%S")
    st_new = round(st.tm_mday+st.tm_hour/24+st.tm_min/(60*24),5)
    PS_j.append(st_new)
# PE_j: the End Time of jth pairing (day)
PE_j = [[]]
for j in range(1,n+1):
    temp = Main_Sheet.cell_value(j,10)+':00'
    et = time.strptime((temp), "%m/%d/%Y %H:%M:%S")
    et_new = round(et.tm_mday+et.tm_hour/24+et.tm_min/(60*24),5)
    PE_j.append(et_new)

# the number of crew memebers/pairings/days/layovers
dn = floor(max(PR_j[1:]))
#ln = Pairing_Layover.ncols - 1

# LN_j: the number of legs of jth pairing
LN_j = [[]]
for j in range(1,n+1):
    LN_j.append(int(Main_Sheet.cell_value(j,4)))

# LD_j: the number of days of jth pairing   
LD_j = [[]]
for j in range(1,n+1):
    LD_j.append(int(Main_Sheet.cell_value(j,3)))

# LH_j: the duty hours of jth pairing
LH_j = [[]]
for j in range(1,n+1):
    LH_j.append(int(Main_Sheet.cell_value(j,7)))

# BH_j: the block hours of jth pairing
BH_j = [[]]
for j in range(1,n+1):
    BH_j.append(int(Main_Sheet.cell_value(j,8)))

# DO_jd: jth pairing has dth day to work/off
DO_jd = [[]]
for j in range(1,n+1):
    row = [0]*dn
    row.insert(0,[])
    for d in range(floor(PS_j[j]), ceil(PR_j[j])):
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
    if Main_Sheet.cell_value(j,1) != '-':
        L_j.append(1)
    else:
        L_j.append(0)

'''Prefrence data reading'''
'''
# CP1_id: ith crew member prefers dth day to work/off
CP1_id = [[]]
for i in range(1,m+1):
    row = [[]]
    for d in range(1,dn+1):
        row.append(int(CP1.cell_value(i,d)))
    CP1_id.append(row)

# CP_il: ith crew member prefers lth lay-over
CP2_il = [[]]
for i in range(1,m+1):
    row = [[]]
    for l in range(1,ln+1):
        row.append(int(CP2.cell_value(i,l)))
    CP2_il.append(row)


CP3 = Data_File.sheet_by_index(6)
CP3_i = [[]]
CP3_c = [[]] 
for i in range(1,5):
    row = [[]]
    for j in range(1,4):
        row.append(CP3.cell_value(i,j))
    CP3_i.append(row)

for j in range(1, 4):
    col = [[]]
    for i in range(1,5):
        if CP3_i[i][j] != '-':
            col.append(i)
    CP3_c.append(col)

CP3_leq = [[]]
if len(CP3_c[1]):
    for i in range(CP3_c[1][1], CP3_c[1][1]+len(CP3_c[1])-1):
        CP3_leq.append(CP3.cell_value(i,1))
else 

CP3_eql = [[]]
if len(CP3_c[2]):
    for i in range(CP3_c[2][1], CP3_c[2][1]+len(CP3_c[2])-1):
        CP3_eql.append(CP3.cell_value(i,2))

CP3_geq = [[]]
if len(CP3_c[3]):
    for i in range(CP3_c[3][1], CP3_c[3][1]+len(CP3_c[3])-1):
        CP3_geq.append(CP3.cell_value(i,3))

CP4 = Data_File.sheet_by_index(7)
CP4_i = [[]]
CP4_c = [[]] 
for i in range(1,5):
    row = [[]]
    for j in range(1,4):
        row.append(CP4.cell_value(i,j))
    CP4_i.append(row)

for j in range(1, 4):
    col = [[]]
    for i in range(1,5):
        if CP4_i[i][j] != '-':
            col.append(i)
    CP4_c.append(col)

CP4_leq = [[]]
if len(CP4_c[1]):
    for i in range(CP4_c[1][1], CP4_c[1][1]+len(CP4_c[1])-1):
        CP4_leq.append(CP4.cell_value(i,1))

CP4_eql = [[]]
if len(CP4_c[2]):
    for i in range(CP4_c[2][1], CP4_c[2][1]+len(CP4_c[2])-1):
        CP4_eql.append(CP4.cell_value(i,2))

CP4_geq = [[]]
if len(CP4_c[3]):
    for i in range(CP4_c[3][1], CP4_c[3][1]+len(CP4_c[3])-1):
        CP4_geq.append(CP4.cell_value(i,3))
'''