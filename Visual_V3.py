# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 01:19:54 2018

@author: Enock
"""

# coding=UTF-8

from Model_V3 import x_nonzero, PS_j, PE_j, y_nonzero, dn
from Summary_V3 import df as summary,e
import pandas as pd
import io
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
plt.rcParams['axes.unicode_minus']=False # to use to display negative sign correctly  



df = pd.DataFrame(columns=["Crewmember", "Start", "Finish","Pairing"])
for i,j in x_nonzero:
    df = df.append({'Crewmember':int(i),'Start':PS_j[j],'Finish':PE_j[j],'Pairing':str(j)},ignore_index=True)
height=8 # rectangular height (should be the mutlipty of 2)
interval=4 #
colors = ("turquoise","crimson","black","red","yellow","green","brown","blue", "turquoise", "crimson","black") 
x_label="schdule" # set x label
df["Diff"] = df.Finish - df.Start
fig,ax=plt.subplots(figsize=(6,3))
labels=[]
count=0


for i,Crewmember in enumerate(df.groupby("Crewmember")):
    labels.append(Crewmember[0])
    data=Crewmember[1]
    for index,row in data.iterrows():
        ax.broken_barh([(row["Start"],row["Diff"])], ((height+interval)*i+interval,height), facecolors=colors[(i%11)])
        #plt.text(row["Start"], (height+interval)*(i+1),row['Pairing'],fontsize='x-small')  
        if(row["Finish"]>count):
            count=row["Finish"]
ax.set_ylim(0, (height+interval)*len(labels)+interval)
ax.set_xlim(0, count+1)
ax.set_xlabel(x_label)
ax.set_yticks(range(5*(interval+int(height/2)),(height+interval)*len(labels),(height+interval)*5))
ax.set_yticklabels(labels[4::5])
#ymajorLocator = MultipleLocator(23) 
#ax.yaxis.set_major_locator(ymajorLocator)
xmajorLocator = MultipleLocator(5)
ax.xaxis.set_major_locator(xmajorLocator)
xminorLocator = MultipleLocator(1)
ax.xaxis.set_minor_locator(xminorLocator)
#ax.set_xticks(range(dn+2))
#ax.grid(True) # show grids
ax.xaxis.grid(True, which='minor') 
#ax.yaxis.grid(True) # show y grid
plt.savefig('gantt.png',dpi=800)
plt.show()
#print(summary)