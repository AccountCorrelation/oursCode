# -*- coding:  UTF-8 -*-
#
from numpy import *
#
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

#
def loadGraphDict(fileName):#
    dataDict_out = {};dataDict_in = {}
    fx = open(fileName)
    for line in fx.readlines():#
        lineArr = re.split(' |,|\t',line.strip())#
        lenth=len(lineArr)
        
        if(lenth<2): 
            break;
        if(lineArr[0] not in dataDict_out.keys()):
            dataDict_out[str(lineArr[0])]=[str(lineArr[1])]
#
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[1] not in dataDict_out[str(lineArr[0])]):
            dataDict_out[str(lineArr[0])].append(str(lineArr[1]))
#
    #
        if(lineArr[1] not in dataDict_in.keys()):
            dataDict_in[str(lineArr[1])]=[str(lineArr[0])]#
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[0] not in dataDict_in[str(lineArr[1])]):
            dataDict_in[str(lineArr[1])].append(str(lineArr[0]))#
    return dataDict_out,dataDict_in

#
def walk(graphDict,num_paths,walkfile,flag):
    walkList=[]#
    f1=open(walkfile,'a+')
    for j in range(int(num_paths)): #
        nodes=list(graphDict.keys())
	random.Random(0).shuffle(nodes)   #
    	for keyStartNode in nodes: #
            #walkList.append(keyStartNode
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

#2.
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



#
def start(father,numpaths,filename='foursquare_following_add'):
    #father="data0/"
    #
    xDict_out,xDict_in=loadGraphDict(father+'foursquare_following_add')
    #print "xDict=",xDict
    yDict_out,yDict_in=loadGraphDict(father+'twitter_following_add')
    #print "yDict=",yDict
    while(numpaths!='stop'):
        #
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
        print "plase input walk numpaths"
        numpaths = raw_input()


if __name__=="__main__":
    nLen = len(sys.argv);
    for i in range(0, nLen):  
        print("argv %d:%s" %(i, sys.argv[i]));  
    father=str(sys.argv[1])
    numpaths=int(sys.argv[2])
    start(str(father),int(numpaths))
