# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 01:19:54 2018

@author: Dennis
"""

# coding=UTF-8
from Model_V1 import x_nonzero, PS_j, PR_j
import pandas as pd
import io
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签  
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号  

'''
PS_j = [[],8.2,2.8,6.3,4.9,1.6,2.3,5.3,8.3,8.7,4.8]
PR_j = [[],10.3,4.7,7.3,6.8,2.7,4.6,8.2,10.3,10.6,6.6]
'''

df = pd.DataFrame(columns=["Crewmember", "Start", "Finish","Pairing"])
for i,j in x_nonzero:
    df = df.append({'Crewmember':'C'+str(i),'Start':PS_j[j],'Finish':PR_j[j],'Pairing':str(j)},ignore_index=True)
height=16 # 柱体高度，设为2的整数倍，方便Y轴label居中，如果设的过大，柱体间的间距就看不到了，需要修改下面间隔为更大的值
interval=4 # 柱体间的间隔
colors = ("turquoise","crimson","black","red","yellow","green","brown","blue", "turquoise", "crimson","black") # 颜色，不够再加
x_label="schdule" # 设置x轴label
df["Diff"] = df.Finish - df.Start
fig,ax=plt.subplots(figsize=(6,3))
labels=[]
count=0
for i,Crewmember in enumerate(df.groupby("Crewmember")):
    labels.append(Crewmember[0])
    data=Crewmember[1]
    for index,row in data.iterrows():
        ax.broken_barh([(row["Start"],row["Diff"])], ((height+interval)*i+interval,height), facecolors=colors[i])
        plt.text(row["Start"], (height+interval)*(i+1),row['Pairing'],fontsize='x-small')  
        if(row["Finish"]>count):
            count=row["Finish"]
ax.set_ylim(0, (height+interval)*len(labels)+interval)
ax.set_xlim(0, count+1)
ax.set_xlabel(x_label)
ax.set_yticks(range(interval+int(height/2),(height+interval)*len(labels),(height+interval)))
ax.set_yticklabels(labels)
ax.set_xticks(range(32))
#ax.grid(True) # 显示网格
ax.xaxis.grid(True) # 只显示x轴网格
#ax.yaxis.grid(True) # 只显示y轴网格
plt.savefig('gantt.png',dpi=800)
plt.show()