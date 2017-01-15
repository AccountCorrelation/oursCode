# -*- coding:  UTF-8 -*-
#科学计算包
from numpy import *
import numpy as np 
#import node2vec
#import networkx as nx
#运算符模块
import operator
import sys;
import time
import gc;
import re;
#listdir
from os import listdir


#第五部分：预测所有关联账户

def tpredict(all_testlist,tpredictPair,xDict,yDict):


    for nodeX in all_testlist:	
        if nodeX in xDict.keys():
            vecX=xDict[nodeX]
	    disDict={}
	    disDictnode=list()
	    disDictdis=list()
	else:	continue
	for nodeY in yDict.keys():
	    vecY=yDict[nodeY]
	    #distance=abs(sum((vecX-vecY)*(vecX-vecY).T))
            distance=-sum(vecX*vecY.T)/(sum(vecX*vecX.T)**(1/2)*sum(vecY*vecY.T)**(1/2))
            ###print distance
	    #distance=1+float(abs(dux-duy))/(float(dux+duy)/2)
            #corelation=1.0/distance
	    disDictnode.append(str(nodeY))
	    disDictdis.append(float(distance))

	i=0

	for index in np.argpartition(disDictdis,kth=100)[:100]:
            eachKey=disDictnode[index];distance=disDictdis[index];
	    #if(i==0 and distance<20*bigdis):
	    if(i==0):
		tpredictPair[nodeX]={eachKey:distance}
		i+=1
	    #elif(distance<20*bigdis and i<5):
	    elif(i<100):
		i+=1
		tpredictPair[nodeX][eachKey]=distance
	    else:
		break
	del(disDictnode,disDictdis)
    return 0

def readVecDict(filename):
    fr=open(filename,'r')
    duDict={}
    for line in fr.readlines():
        lineArr = re.split(' |,|\t',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr)
        if(lenth<2):break;
        now=[]
        for i in lineArr[1:]:
            now.append(float(i))
        duDict[lineArr[0]]=array(now)
    return duDict
        

def start():
    gc.collect()
    print "startTime",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    
    #xDict=readDuDict('modelx.vocab')
    #yDict=readDuDict('modely.vocab')
    xDict=readVecDict('Vector_x.txt')
    yDict=readVecDict('Vector_y.txt')

    all_testlist=list();all_testYlist=list()
    ft=open('testConnect3148.txt','r')
    for line in ft.readlines():
	lineArr = line.strip().split()
        if(len(lineArr)<2):break;
	nodeX=lineArr[0]
	nodeY=lineArr[1]
        all_testlist.append(nodeX)
        all_testYlist.append(nodeY)
    ft.close()
        
    print "*******************得到data了*******************"

  
     

########################test##################################
    tpredictPair={}
    tpredict(all_testlist,tpredictPair,xDict,yDict)
    #判断准确度
    testrightItem100=0.0;
    testrightItem30=0.0;
    testrightItem15=0.0;
    testright10=0.0
    testright8=0.0
    testright5=0.0
    testright3=0.0
    testright1=0.0
    fr=open('result_cos.txt','a')
    for j in range(0,len(all_testlist)):
	#if ('a'+str(node)==tpredictPair[node]):
	    #rightItem+=1
        now=0.0
        node=all_testlist[j]
        if(node not in tpredictPair.keys()):print 'node',node;continue
        fr.write('%s '%str(node))
	for(dictPnode,distance) in sorted(tpredictPair[node].items(),key=operator.itemgetter(1)):
            now+=1
            flag=0
            fr.write('%s '%(str(dictPnode) ))
	    if(all_testYlist[j]==dictPnode):
		testrightItem100+=1
		if(now==1): 
                    testright1+=1
		if(now<=3): 
                    testright3+=1
		if(now<=5): 
                    testright5+=1
		if(now<=8): 
                    testright8+=1
		if(now<=10): 
                    testright10+=1
		if(now<=15):
		    testrightItem15+=1
		if(now<=30):
                    flag=1
		    testrightItem30+=1
		break
        fr.write('\n')
      
    if(len(tpredictPair)>0):
	print "前100测试准确率为：",(testrightItem100/len(tpredictPair))
	print "前30测试准确率为：",(testrightItem30/len(tpredictPair))
	print "前15测试准确率为：",(testrightItem15/len(tpredictPair))
	print "前10测试准确率为：",(testright10/len(tpredictPair))
	print "前8测试准确率为：",(testright8/len(tpredictPair))
	print "前5测试准确率为：",(testright5/len(tpredictPair))
	print "前3测试准确率为：",(testright3/len(tpredictPair))
	print "前1测试准确率为：",(testright1/len(tpredictPair))
        print "测试条数为：",(len(tpredictPair))
    else:
	print "出错了，测试准确率，被0除！！"
    del(tpredictPair)

    print "（计算测试集预测结果和test准确度）完成时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
   
    gc.collect()
if __name__=="__main__":
    start()
