# -*- coding:  UTF-8 -*-
#科学计算包
from numpy import *
#运算符模块
import operator
import sys
import re
#listdir
from os import listdir
def start():
    mapItems=0.0
    fp=open('result_cos.txt','r')
    for line in fp.readlines():
        lineArr = re.split(' |,|\t',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr) 
        if(lenth==101 and lineArr[0].lower()!=lineArr[lenth-1].lower()):
            continue;
        for j in range(1,lenth):
            if(lineArr[0].lower()==lineArr[j].lower()):
                mapItems+=1.0/(j)    
    map=mapItems/1050
    print 'map',map   
    fp.close()

if __name__=="__main__":
    #filename=sys.argv[1]
    start()

