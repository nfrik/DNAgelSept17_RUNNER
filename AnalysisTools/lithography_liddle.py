__author__ = 'nfrik'
import numpy as np
from scipy import integrate
import pylab as P
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
import random

dic = {"STM":[1e-1,1e-21,0,[0,17]],"H2 Pass":[1e0,1e-15,0,[0,-14]],"eBeam Inorganic Resist":[10**0.2,1e-15,0,[35,10]],"FIB":[10**1.5,10**-12.5,0,[-10,10]],\
		"Si AFM":[10*1.3,1e-10,0,[-13,-10]],"Gauss eBeam":[10**2,10**-7,0,[-25,25]],"Shaped Beam":[10**2.5,1e-5,0,[30,10]],"Opt. Litho":[10**1.5,10**-3,0,[-10,-12]],\
		"":[10**0.5,10**-4.0,2,[-15,-10]],"Inkjet + Letterpress":[1e4,1e1,0,[-10,0]],"NIL R2R":[10,10,2,[5,17]],"Diblock SA":[10**0.5,10,2,[10,-25]]}#"Particle SA":[10,10,4,[0,10]]}

x=[]
y=[]
z=[]
labc=[]
l=[]

for k in dic.keys():
	y.append(dic[k][0])
	x.append(dic[k][1])
	z.append(dic[k][2])
	labc.append(dic[k][3])
	l.append(k)
print x,y


# plt.loglog(x,y,'ro',markersize=15)
s=[100+20**n for n in z]
c=[n*0.1/len(z)+0.5 for n in range(len(z))]
# plt.scatter(x,y,marker='o',c='b',s=s,label='stuff')
fig = plt.figure()
ax = plt.gca()
ax.scatter(x,y,s=s,c=c,edgecolors='none',cmap=cm.gist_heat)
ax.set_ylim([10**-1.5,10**4.5])
ax.set_xlim([10**-23,10**3])
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xticks([1e-21,1e-15,1e-10,1e-5,10])
plt.xlabel(r'Throughput $(m^2/s)$')
plt.ylabel("Resolution (nm)")
plt.grid()

for label, x, y, lc in zip(l, x, y, labc):
    plt.annotate(
        label,
        xy = (x, y), xytext = (lc[0],lc[1]),
        textcoords = 'offset points', ha = 'right', va = 'bottom')

# for l, x,y in zip(l,x,y):
# 	plt.annotate(l, xy=(x,y), textcoords='offset points')

print x
print y
print z
print c
plt.show()