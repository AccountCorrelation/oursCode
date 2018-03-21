# -*- coding:  UTF-8 -*-
#
from numpy import *
import numpy as np 
#import node2vec
#import networkx as nx
#
import operator
import sys;
import time
import gc;
import re;
#listdir
from os import listdir


#

def tpredict(all_testlist,tpredictPair,xDict,yDict):


    for nodeX in all_testlist:	
        if nodeX in xDict.keys():
            dux=xDict[nodeX]
	    disDict={}
	    disDictnode=list()
	    disDictdis=list()
	else:	continue
	for nodeY in yDict.keys():
	    duy=yDict[nodeY]
	    distance=1+float(abs(dux-duy))/(float(dux+duy)/2)
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

def readDuDict(filename):
    fr=open(filename,'r')
    duDict={}
    for line in fr.readlines():
        lineArr = re.split(' |,|\t',line.strip())#
        lenth=len(lineArr)
        if(lenth<2):break;
        duDict[lineArr[0]]=float(lineArr[2])
    return duDict
        

def start():
    gc.collect()
    print "startTime",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    
    #xDict=readDuDict('modelx.vocab')
    #yDict=readDuDict('modely.vocab')
    xDict=readDuDict('foursquare_communitydu_4.tsv')
    yDict=readDuDict('twitter_communitydu_t.tsv')

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
        
    print "*******************data*******************"

  
     

########################test##################################
    tpredictPair={}
    tpredict(all_testlist,tpredictPair,xDict,yDict)
    #
    testrightItem100=0.0;
    testrightItem30=0.0;
    testrightItem15=0.0;
    testright10=0.0
    testright8=0.0
    testright5=0.0
    testright3=0.0
    testright1=0.0
    fr=open('result.txt','a')
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
	print "top 100 test accuracy：",(testrightItem100/len(tpredictPair))
	print "top 30 test accuracy：",(testrightItem30/len(tpredictPair))
	print "top 15 test accuracy：",(testrightItem15/len(tpredictPair))
	print "top 10 test accuracy：",(testright10/len(tpredictPair))
	print "top 8 test accuracy：",(testright8/len(tpredictPair))
	print "top 5 test accuracy：",(testright5/len(tpredictPair))
	print "top 3 test accuracy：",(testright3/len(tpredictPair))
	print "top 1 test accuracy：",(testright1/len(tpredictPair))
        print "test items：",(len(tpredictPair))
    else:
	print "error，test accuracy，division 0！！"
    del(tpredictPair)

    print "compute and predict end time:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
   
    gc.collect()
if __name__=="__main__":
    start()
