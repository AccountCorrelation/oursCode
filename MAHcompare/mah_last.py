# -*- coding:  UTF-8 -*-
#科学计算包
from numpy import *
import numpy
#运算符模块
import operator
import sys;
import re
import gc
import scipy.sparse.linalg as linalg
import scipy.io as sio
#listdir
from os import listdir
import time
#random
import random
from random import shuffle
#第一部分：获得图中边的字典表示
def loadGraphDict(fileName):#初始化待处理数据
    dataDict = {}
    fx = open(fileName)
    for line in fx.readlines():#m行
        lineArr = re.split(' |,|\t',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr)
        
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
#第一部分：获得图中边的字典表示
def loadNodeList(fileName):#初始化待处理数据
    nodeNameList =[];nodeDuList=[];
    fx = open(fileName)
    j=0
    for line in fx.readlines():#m行
        lineArr = re.split(' |,|\t',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr)
        j+=1
        if(lenth<2): 
            break;
        if lineArr[0] not in nodeNameList:
            nodeNameList.append(lineArr[0])
            nodeDuList.append(int(lineArr[1]))
    return nodeNameList,nodeDuList

def getIDbyName(name,xlist):
    nowid=0
    for i in xlist:
        if(name==i):returnid=nowid;break;
        nowid+=1
    return returnid

def getsamefriendlenth(a,b):
    sames=[val for val in a if val in b]
    return len(sames)


#接下来梳理community关系
def loadHHT(fileName,xnamelist):#初始化待处理数据
    n=len(xnamelist)
    HHT=array([[0]*n]*n)
    dataDict = loadGraphDict(fileName)
    j=0;i=0
    for i in range(n):#
        for j in range(i,n):
            node1_friends=dataDict[xnamelist[i]]
            node2_friends=dataDict[xnamelist[j]]
            data=float(getsamefriendlenth(node1_friends,node2_friends))
            HHT[i][j]=data
            HHT[j][i]=data
            j+=1
        i+=1
    print 'HHT=',len(HHT),len(HHT[0])
    return array(HHT)

def banjia(xL,yL):
    #print xL
    xL=array(xL);yL=array(yL)
    L=[];l=2098;m=5313-l;n=5120-l;
    i=0;j=0;k=0       
    for i in range(l):
        nowraw=[]
        for j in range(l):
            nowraw.extend([xL[i][j]+yL[i][j]])
        nowraw.extend(xL[i][l:])
        nowraw.extend(yL[i][l:])
        print i,'=',len(nowraw) 
        L.append(nowraw)
    i=0
    for i in range(l,l+m):
        nowraw=[]
        nowraw.extend(xL[i][:])
        nowraw.extend([0]*(n))
        print i,'=',len(nowraw) 
        L.append(nowraw)
    i=0
    for i in range(l,l+n):
        nowraw=[]
        nowraw.extend(yL[i][:l])
        nowraw.extend([0]*(m))
        nowraw.extend(yL[i][l:])
        print i,'=',len(nowraw) 
        L.append(nowraw)
    #print len(nowraw)    
    return array(L)

def banjiad(xD,yD):
    L=[];l=2098;m=5313-l;n=5120-l;
    i=0;k=0;
    nowraw=[]
    for i in range(l):
        nowraw.append(xD[i][i]+yD[i][i])
    for i in range(l,l+m):
        nowraw.append(xD[i][i])
    for i in range(l,l+n):
        nowraw.append(yD[i][i])
    L=diag(nowraw)
    return array(L)

   
def record(V,xNodeList,yNodeList):  
    fwx=open('data400/Vector_x.txt','w')
    for i in range(2098,5313):
        fwx.write('%s '%xNodeList[i])
        for j in V[i][:]:
            fwx.write('%f '%j)
        fwx.write('\n')
    fwy=open('data400/Vector_y.txt','w')
    i=0
    for i in range(2098,5120):
        fwy.write('%s '%yNodeList[i])
        for j in V[5313+i-2098][:]:
            fwy.write('%f '%j)
        fwy.write('\n')
    return 0

def recordlist(vec,filename):  
    fwx=open(filename,'w')
    for i in vec:
        for j in i:
            fwx.write('%d '%int(j))
        fwx.write('\n')
    return 0

def readflist(filename): 
    fl=[] 
    fr=open(filename,'r')
    for line in fr.readlines():
        lineArr = re.split(' |,|\t',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr)
        if(lenth<2): 
            break;
        nowraw=[]
        for i in lineArr:
            nowraw.append(int(i))
        fl.append(nowraw)
    return array(fl)


def start():
    gc.collect()
    print "（开始时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    xNodeNameList,xNodeDuList=loadNodeList('x_du.txt')
    yNodeNameList,yNodeDuList=loadNodeList('y_du.txt')
    '''xHHT=array(loadHHT('foursquare_following',xNodeNameList));
    xD=diag(xNodeDuList);xL=xD-xHHT;
    recordlist(xHHT,'xHHT.txt');   recordlist(xL,'xL.txt');    recordlist(xD,'xD.txt');
    xHHT= readflist('xHHT.txt');   xL=readflist('xL.txt');    xD=readflist('xD.txt');
    print "（x的H,D完成时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    yHHT=array(loadHHT('twitter_following',yNodeNameList));
    yD=diag(yNodeDuList);yL=yD-yHHT;
    recordlist(yHHT,'yHHT.txt');   recordlist(yL,'yL.txt');    recordlist(yD,'yD.txt');
    yHHT= readflist('yHHT.txt');   yL=readflist('yL.txt');    yD=readflist('yD.txt');
    print "（y的H,D完成时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    L=banjia(xL,yL)
    D=banjiad(xD,yD)
    #matL=matrix(L)
    #matD=matrix(D)
    matL=L
    matD=D
    recordlist(L,'L.txt');   recordlist(D,'D.txt'); 
    
    matL=readflist('L.txt');matD=readflist('D.txt');
    #recordlist(matL,'L.txt');   recordlist(matD,'D.txt') 
    #sio.savemat("LD.mat",{"L":matL,"D":	matD},oned_as='row')
    print "（L,D完成时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))'''
    #Lamda,V=linalg.eigs(A=matL,k=400,M=matD)
    V=sio.loadmat("V400.mat")["V"]
    record(V,xNodeNameList,yNodeNameList)
    print "（Lamda,V完成时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return 0

if __name__=="__main__":
    start()



