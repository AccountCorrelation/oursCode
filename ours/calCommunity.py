# -*- coding:  UTF-8 -*-
#科学计算包
from numpy import *
#运算符模块
import operator
import sys;
import re
#listdir
from os import listdir
#random
import random
from random import shuffle

#第一部分：获得图中边的字典表示
def loadGraphDict(father='data/',fileName='x3.txt'):#初始化待处理数据
    dataDict = {}
    fx = open(father+fileName)
    j=0
    for line in fx.readlines():#m行
        lineArr = re.split(' |,|\t',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr)
        if(j%10000==0):print 'j=',j
        j+=1
        if(lenth<2): 
            break;
        if(lineArr[0] not in dataDict.keys()):
            dataDict[str(lineArr[0])]=[str(lineArr[1])]
#建立以某个节点的相邻边集权重字典
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[1] not in dataDict[str(lineArr[0])]):
            dataDict[str(lineArr[0])].append(str(lineArr[1]))
#在该节点的相邻边集上加一条新边
    #有向图则只一边，无向图加两次。
        if(lineArr[1] not in dataDict.keys()):
            dataDict[str(lineArr[1])]=[str(lineArr[0])]#建立以某个节点的相邻边集权重字典
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[0] not in dataDict[str(lineArr[1])]):
            dataDict[str(lineArr[1])].append(str(lineArr[0]))#在该节点的相邻边集上加一条新边
    return dataDict

#接下来梳理community关系
def loadCircleDict(father='data/',fileName='x3.txt'):#初始化待处理数据
    communityID=0
    communityDict={}
    communityDict['0']=0
    fx = open(father+fileName)
    j=0
    for line in fx.readlines():#m行
        lineArr = re.split(' |,|\t',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr)
        if(j%10000==0):print 'i=',j
        j+=1
        if(lenth<1): 
            break;
        if(lineArr[0] not in communityDict.keys() and lineArr[1] not in communityDict.keys()):
            communityID+=1
            communityDict[str(lineArr[0])]=communityID
            communityDict[str(lineArr[1])]=communityID
            continue;
        if(lineArr[0] in communityDict.keys() and lineArr[1] in communityDict.keys()):
            communityID+=1
            a=communityDict[str(lineArr[0])];
            b=communityDict[str(lineArr[1])];
            if(a!=b):
                if(a>b):big=a;small=b;
                else: big=b;small=a;
                for k in communityDict.keys():
                    if(communityDict[k]==big):
                        communityDict[k]=small
                print small,'=',big
                f1=open(father+'hebing.txt','a')
                f1.write('%d=%d\n'%( small,big ))
                f1.close()
            continue;
        if(lineArr[0] in communityDict.keys()):
            communityDict[str(lineArr[1])]=communityDict[str(lineArr[0])]
            continue;
        if(lineArr[1] in communityDict.keys()):
            communityDict[str(lineArr[0])]=communityDict[str(lineArr[1])]
            continue;    
    return communityDict

def start(father='data/',fileName='x3.txt'):

    communityDict=loadCircleDict(father,fileName)
    fww=open(father+'community1_t.txt','w')
    for k in communityDict.keys():
        fww.write('%s\t%d\n'%(k,communityDict[k] ) )
    fww.close()
    dataDict=loadGraphDict(father,fileName);
    fwww=open(father+'communitydu_t.txt','w')
    for k in dataDict.keys():
        fwww.write('%s\t%d\t%d\n'%(k,communityDict[k],len(dataDict[k]) ) )
    fwww.close()
    return 0

if __name__=="__main__":
    start(father='data/',fileName='twitter_following')
