# -*- coding: utf-8 -*-

import pandas as pd
import io
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from Model import x_nonzero, PS_j, PE_j, y_nonzero, dn

'''General Setting'''
plt.rcParams['axes.unicode_minus']=False #display negative sign correctly  

#read data frame 
df = pd.DataFrame(columns=["Crewmember", "Start", "Finish","Pairing"])
for i,j in x_nonzero:
    df = df.append({'Crewmember':int(i),'Start':PS_j[j],'Finish':PE_j[j],'Pairing':str(j)},ignore_index=True)
df["Diff"] = df.Finish - df.Start

'''Create Total Graph'''
def gannt(df,index):
    name = 'gantt'+str(index)+'.png' #rename
    height=8 #rectangular height (should be the mutliply of 2)
    interval=4 #rectangular interval
    colors = ("turquoise","crimson","black","red","yellow","green","brown","blue", "turquoise", "crimson","black") #set colors 
    x_label="Schedule" #set x label
    y_label="Crew_Member" #set y label
    fig,ax=plt.subplots(figsize=(12,6))
    labels=[]
    count=0
    for i,Crewmember in enumerate(df.groupby("Crewmember")):
        labels.append(Crewmember[0])
        data=Crewmember[1]
        for index,row in data.iterrows():
            ax.broken_barh([(row["Start"],row["Diff"])], ((height+interval)*i+interval,height), facecolors=colors[(i%11)])
            if(row["Finish"]>count):
                count=row["Finish"]
    ax.set_ylim(0, (height+interval)*len(labels)+interval)
    ax.set_xlim(0, count+1)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_yticks(range(5*(interval+int(height/2)),(height+interval)*len(labels),(height+interval)*5))
    ax.set_yticklabels(labels[4::5])
    xmajorLocator = MultipleLocator(5)
    ax.xaxis.set_major_locator(xmajorLocator)
    xminorLocator = MultipleLocator(1)
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.xaxis.grid(True, which='minor') 
    plt.savefig(name,dpi=2000)
    plt.show()

gannt(df,92) #run the generating function

'''Create Subgraph'''
# first subgraph for crew member #1-#10
def gannt10(df,index):
    name = 'gantt'+str(index)+'.png'
    height=8
    interval=4
    colors = ("turquoise","crimson","black","red","yellow","green","brown","blue", "turquoise", "crimson","black") 
    x_label="Schedule"
    y_label="Crew_Member"
    fig,ax=plt.subplots(figsize=(12,6))
    labels=[]
    count=0
    for i,Crewmember in enumerate(df.groupby("Crewmember")):
        labels.append(Crewmember[0])
        data=Crewmember[1]
        for index,row in data.iterrows():
            ax.broken_barh([(row["Start"],row["Diff"])], ((height+interval)*i+interval,height), facecolors=colors[(i%11)])
            plt.text(row["Start"], (height+interval)*(i+1),row['Pairing'],fontsize='x-small')  
            if(row["Finish"]>count):
                count=row["Finish"]
    ax.set_ylim(0, (height+interval)*len(labels)+interval)
    ax.set_xlim(0, count+1)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_yticks(range((interval+int(height/2)),(height+interval)*len(labels),(height+interval)))
    ax.set_yticklabels(labels)
    xmajorLocator = MultipleLocator(5)
    ax.xaxis.set_major_locator(xmajorLocator)
    xminorLocator = MultipleLocator(1)
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.xaxis.grid(True, which='minor') 
    plt.savefig(name,dpi=2000)
    plt.show()

# routine to generate all of the subgraphs
i = 1
while i < 92:
    df1 = df[df.Crewmember >= i]
    df2 = df1[df1.Crewmember <= min(i+9,92)]
    gannt10(df2,i)
    i = i + 10