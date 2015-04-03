__author__ = 'nfrik'


import os
from numpy import *
import numpy
from scipy import integrate
import pylab as P


strl = "Fitness for this run:"
rootpath = "/Users/nfrik/Documents/Research_RUNNER/"

data=[8,8,8,8,8,192]
list=[[] for i in range(len(data))]

for i in range(len(data)):
    f=open(rootpath+"DNAngel"+str(data[i])+"_XTRAtest_xor/N"+str(data[i])+"_2_sample.log")
    for line in f:
        if strl in line:
               list[i].append(float(line.replace(strl," ")))
    f.close()


for i in range(len(data)):
    P.subplot(int('23'+str(i+1)))
    n,bins,patches = P.hist(list[i],bins=linspace(0,1,20),log=True)
    P.title('N='+str(data[i])+' XOR')
    P.xlabel('fitness')
    P.ylabel('# occurences')
    P.grid(True)

P.show()
