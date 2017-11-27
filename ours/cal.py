# -*- coding:  UTF-8 -*-
#科学计算包
from numpy import *
#运算符模块
import operator
import sys
import re
#listdir
from os import listdir
#word2vec
from gensim import corpora, models, similarities
from gensim import utils, matutils
from gensim.models import word2vec
from gensim import *


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



#START是主函数
def start(filename):
    #father="data10/"
    #第一部分：获得图中边的字典表示
    xDict=loadGraphDict(filename)
    #print "xDict=",xDict
    #yDict=loadGraphDict(father+'y2.txt')
    #print "yDict=",yDict

    #fx=open('x.txt')
    #fc=open(father+'trainConnect.txt','w')
    #ft=open(father+'testConnect.txt','w')

    #randomIter=random.randint(0, 2)
    #nowIter=0
    i=0
    sumdu=0.0
    for node in xDict.keys():
        #lineArr = line.strip().split()
        sumdu+=len(xDict[node])
        i+=1
    print("共有几条="),i
    print("节点平均度为="),float(sumdu/i)



    fp=open('data/xDict.txt','w')
    for li,lis in xDict.items():
        fp.write('%s '%str(li))
        for h in lis:
            fp.write('%s '%str(h))
        fp.write('\n')
    fp.close()



    return i,float(sumdu/i),xDict
    


    #fc.close()
    #ft.close()

if __name__=="__main__":
    filename=sys.argv[1]
    start(filename)
