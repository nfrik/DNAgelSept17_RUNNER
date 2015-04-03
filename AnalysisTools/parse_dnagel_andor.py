__author__ = 'nfrik'

import os
from numpy import *
import numpy
from scipy import integrate
import pylab as P

strl = "Fitness for this run:"


f=open("/Users/nfrik/Documents/Research3/DNAngel64_XTRAtest_xor/N64_2_sample.log")
list0=[]
for line in f:
    if strl in line:
         # print float(line.replace(strl," "))
           list0.append(float(line.replace(strl," ")))

f.close()

f=open("/Users/nfrik/Documents/Research3/DNAngel128_XTRAtest_xor/N128_2_sample.log")
list1=[]
for line in f:
    if strl in line:
         # print float(line.replace(strl," "))
           list1.append(float(line.replace(strl," ")))

f.close()

f=open("/Users/nfrik/Documents/Research3/DNAngel256_XTRAtest_xor/N256_2_sample.log")
list2=[]
for line in f:
    if strl in line:
         # print float(line.replace(strl," "))
           list2.append(float(line.replace(strl," ")))
f.close()

f=open("/Users/nfrik/Documents/Research3/DNAngel512_XTRAtest_xor/N512_2_sample.log")
list3=[]
for line in f:
    if strl in line:
         # print float(line.replace(strl," "))
           list3.append(float(line.replace(strl," ")))
f.close()

f=open("/Users/nfrik/Documents/Research3/DNAngel1024_XTRAtest_xor/N1024_2_sample.log")
list4=[]
for line in f:
    if strl in line:
         # print float(line.replace(strl," "))
           list4.append(float(line.replace(strl," ")))
f.close()

f=open("/Users/nfrik/Documents/Research3/DNAngel2048_XTRAtest_xor/N2048_2_sample.log")
list5=[]
for line in f:
    if strl in line:
         # print float(line.replace(strl," "))
           list5.append(float(line.replace(strl," ")))

f.close()

P.subplot(231)
n,bins,patches = P.hist(list0,bins=linspace(0,1,30))
P.title('N=64 XOR')
P.xlabel('fitness')
P.ylabel('# occurences')
P.grid(True)

P.subplot(232)
n,bins,patches = P.hist(list1,bins=linspace(0,1,30))
P.title('N=128 XOR')
P.xlabel('fitness')
P.ylabel('# occurences')
P.grid(True)


P.subplot(233)
n,bins,patches = P.hist(list2,bins=linspace(0,1,30))
P.title('N=256 XOR')
P.xlabel('fitness')
P.ylabel('# occurences')
P.grid(True)

P.subplot(234)
n,bins,patches = P.hist(list3,bins=linspace(0,1,30))
P.title('N=512 XOR')
P.xlabel('fitness')
P.ylabel('# occurences')
P.grid(True)

P.subplot(235)
n,bins,patches = P.hist(list4,bins=linspace(0,1,30))
P.title('N=1024 XOR')
P.xlabel('fitness')
P.ylabel('# occurences')
P.grid(True)

P.subplot(236)
n,bins,patches = P.hist(list5,bins=linspace(0,1,30))
P.title('N=2048 XOR')
P.xlabel('fitness')
P.ylabel('# occurences')
P.grid(True)

P.show()
