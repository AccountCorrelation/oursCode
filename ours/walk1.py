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
#word2vec
from gensim import corpora, models, similarities
from gensim import utils, matutils
from gensim.models import word2vec
from gensim import *

#第一部分：获得图中边的字典表示
def loadGraphDict(fileName):#初始化待处理数据
    dataDict_out = {};dataDict_in = {}
    fx = open(fileName)
    for line in fx.readlines():#m行
        lineArr = re.split(' |,|\t',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr)
        
        if(lenth<2): 
            break;
        if(lineArr[0] not in dataDict_out.keys()):
            dataDict_out[str(lineArr[0])]=[str(lineArr[1])]
#建立以某个节点的相邻边集权重字典
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[1] not in dataDict_out[str(lineArr[0])]):
            dataDict_out[str(lineArr[0])].append(str(lineArr[1]))
#在该节点的相邻边集上加一条新边
    #有向图则只一边，无向图加两次。
        if(lineArr[1] not in dataDict_in.keys()):
            dataDict_in[str(lineArr[1])]=[str(lineArr[0])]#建立以某个节点的相邻边集权重字典
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[0] not in dataDict_in[str(lineArr[1])]):
            dataDict_in[str(lineArr[1])].append(str(lineArr[0]))#在该节点的相邻边集上加一条新边'''
    return dataDict_out,dataDict_in

#第二部分：根据图边字典进行（权重）随机游走得到序列集
def walk(graphDict,num_paths,walkfile,flag):
    walkList=[]#每一项是一条路径
    f1=open(walkfile,'a+')
    for j in range(int(num_paths)): #暂且写成从所有节点开始外循环趟数
        nodes=list(graphDict.keys())
	random.Random(0).shuffle(nodes)   #打乱顺序
    	for keyStartNode in nodes: #暂且写成从每个节点开始循环
            #walkList.append(keyStartNode)
            #nowLength=1
            if len(graphDict[keyStartNode])<1:continue;
            for firstcengNeighbor in graphDict[keyStartNode]:
                walkList.append(keyStartNode);
                walkList.append(firstcengNeighbor)
                nowLength=2
	        RandomWalk(graphDict,walkList,firstcengNeighbor,nowLength)
                if(flag=='in'):
                    walkList=walkList[::-1]
                for e in walkList:
		    f1.write('%s '%(e))
	        f1.write('\n');
                #print 'walkList=',walkList
                walkList=[]
    f1.close()
    return walkList

#2.1递归函数，每次根据权重走一步，走过的边不再走，但水平有限，暂且写个不管权重的随机游走，
def RandomWalk(graphDict,walkList,nowNode,nowLength,walkLength=40):
    #randomIter=random.randint(0, len(graphDict[nowNode]))
    if(nowLength>=walkLength):	
        return 0
    #nowNode1=1
    if nowNode not in graphDict.keys() or len(graphDict[nowNode])<1:return 0;
    nowNode=random.Random().choice(graphDict[nowNode])
    #ik=0.0
    #if(nowNode1 in walkList[-1]):
        #ik+=1
        #nowNode1=random.Random().choice(graphDict[nowNode].keys())
    #nowNode=nowNode1    
    walkList.append(nowNode)
    RandomWalk(graphDict,walkList,nowNode,nowLength+1)

    #nowIter=0
    #for nextNode in graphDict[nowNode].keys():#
        #if(nowIter==randomIter):
	    #nowNode=nextNode
	    #walkList[-1].append(str(nowNode))
	    #RandomWalk(graphDict,walkList,nowNode,nowLength+1)
            #break
        #else:
            #nowIter+=1;continue



#START是主函数
def start(father,numpaths,filename='foursquare_following_add'):
    #father="data0/"
    #第一部分：获得图中边的字典表示
    xDict_out,xDict_in=loadGraphDict(father+'foursquare_following_add')
    #print "xDict=",xDict
    yDict_out,yDict_in=loadGraphDict(father+'twitter_following_add')
    #print "yDict=",yDict
    while(numpaths!='stop'):
        #第二部分：根据图边字典进行随机游走得到序列集
        try:
            numpaths=int(numpaths)
        except EXception:
            print 'error';break;
        walkListX_out=walk(xDict_out,numpaths,walkfile=father+'walk1all_X.txt',flag='out')
        #print "walkListX=",walkListX
        walkListY_out=walk(yDict_out,numpaths,walkfile=father+'walk1all_Y.txt',flag='out')
        #print "walkListY=",walkListY
        walkListX_in=walk(xDict_in,numpaths,walkfile=father+'walk1all_X.txt',flag='in')
        walkListY_in=walk(yDict_in,numpaths,walkfile=father+'walk1all_Y.txt',flag='in')
        print "请输入游走趟数numpaths"
        numpaths = raw_input()


if __name__=="__main__":
    nLen = len(sys.argv);
    for i in range(0, nLen):  
        print("argv %d:%s" %(i, sys.argv[i]));  
    father=str(sys.argv[1])
    numpaths=int(sys.argv[2])
    start(str(father),int(numpaths))
