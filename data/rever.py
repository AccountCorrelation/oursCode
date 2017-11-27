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


#第二部分：根据图边字典进行（权重）随机游走得到序列集
def reverse():
    fx = open('trainConnect3148.txt','r')
    f1=open('trainConnect3148.txt_0','a+')
    for line in fx.readlines():#m行
        lineArr = re.split(' |,|\t',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr)
        
        if(lenth<2): 
            break;
	f1.write('%s\n'%(lineArr[1].lower()))
    f1.close()
    fx.close()
    return 0


if __name__=="__main__":
    reverse();
