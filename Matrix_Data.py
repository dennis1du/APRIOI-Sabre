# -*- coding: utf-8 -*-
#v1+2 v1+3
import xlrd

Data_File = xlrd.open_workbook("Matrix_data_sample.xlsx")

'''Sheets loaded'''
Main_Sheet = Data_File.sheet_by_index(0)
Overlap = Data_File.sheet_by_index(1)
Day_Off = Data_File.sheet_by_index(2)
Pairing_Layover = Data_File.sheet_by_index(3)
CP1 = Data_File.sheet_by_index(5)
CP2 = Data_File.sheet_by_index(6)

'''global data reading'''
# the number of crew memebers/pairings/days/layovers
m = CP1.nrows - 1
n = Main_Sheet.nrows - 2
dn = Day_Off.ncols - 1
ln = Pairing_Layover.ncols - 1

# LN_j: the number of legs of jth pairing
LN_j = [[]]
for j in range(2,n+2):
    LN_j.append(int(Main_Sheet.cell_value(j,4)))

# LD_j: the number of days of jth pairing   
LD_j = [[]]
for j in range(2,n+2):
    LD_j.append(int(Main_Sheet.cell_value(j,3)))

# LH_j: the number of hours of jth pairing
LH_j = [[]]
for j in range(2,n+2):
    LH_j.append(int(Main_Sheet.cell_value(j,7)))

# BH_j: the block hours of jth pairing
BH_j = [[]]
for j in range(2,n+2):
    BH_j.append(int(Main_Sheet.cell_value(j,8)))

#O_gh: the gth pairing and the hth pairing are overlapped/not
O_gh = [[]]
for g in range(1,n+1):
    row = [[]]
    for h in range(1,n+1):
        row.append(int(Overlap.cell_value(g,h)))
    O_gh.append(row)

# DO_jd: jth pairing has dth day to work/off
DO_jd = [[]]
for j in range(1,n+1):
    row = [[]]
    for d in range(1,dn+1):
        row.append(int(Day_Off.cell_value(j,d)))
    DO_jd.append(row)

# LO_jl: jth pairing has lth lay-over
LO_jl = [[]]
for j in range(1,n+1):
    row = [[]]
    for l in range(1,ln+1):
        row.append(int(Pairing_Layover.cell_value(j,l)))
    LO_jl.append(row)

L_j = [[]]
for j in range(1,n+1):
    row = [[]]
    s = 0
    for l in range(1,ln+1):
        s += int(Pairing_Layover.cell_value(j,l))
    if s>=1:
        row.append(1)
    else: row.append(0)
    L_j.append(row)

'''Prefrence data reading'''
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

'''
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


#v2