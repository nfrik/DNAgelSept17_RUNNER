__author__ = 'nfrik'

import os
from numpy import *
import numpy
from scipy import integrate
import pylab as P
import matplotlib.pyplot as plt

repetition = 61
repstr = "Repetition"
outputvals = "Output values:"
statesoccup = "States occupancy:"
fitstr = "Fitness for this run:"
fitness = 0
ttab_cntr = 0
ttab_max = 4

readnext = False

oval=[[] for i in range(ttab_max)]
occup=[[] for i in range(ttab_max)]
# with open("/Users/nfrik/Documents/DNAGelRuns/Research3/DNAngel512_XTRAtest_or/N512_2_sample.log") as f:
with open("/Users/nfrik/Documents/DNAGelRuns/Research_RUNNER/DNAngel256_XTRAtest_and/N256_2_sample.log") as f:
     for line in f:
        if (repstr in line) and (int(line.split()[2]) == repetition):
            readnext = True
        if readnext == True:
            if outputvals in line:
                   #print eval(line.replace(outputvals," "))
                   oval[ttab_cntr]=eval(line.replace(outputvals," "))
            if statesoccup in line:
                   #print eval(line.replace(outputvals," "))
                   occup[ttab_cntr]=(eval(line.replace(statesoccup," ")))
                   ttab_cntr+=1

            if fitstr in line:
               fitness = float(line.replace(fitstr," "))
               ttab_cntr+=1

            if ttab_cntr == ttab_max+1:
               break

f.close()


ax1 = P.subplot(2,2,1)
ax2 = ax1.twinx()

ax3 = P.subplot(2,2,2)
ax4 = ax3.twinx()

ax5 = P.subplot(2,2,3)
ax6 = ax5.twinx()

ax7 = P.subplot(2,2,4)
ax8 = ax7.twinx()

ax1.plot(occup[0],'-',color='r',linewidth=4)
ax1.set_ylabel('occupancy (true nodes - false nodes)')
ax1.set_xlabel('step')
for t1 in ax1.get_yticklabels():
    t1.set_color('r')

ax2.plot( oval[0],'s')
ax2.set_ylabel('Output state ')
ax2.set_ylim([-.1,1.1])
ax2.set_yticks([0,1])
for t2 in ax2.get_yticklabels():
    t2.set_color('b')

ax3.plot(occup[1],'-',color='r',linewidth=4)
ax3.set_ylabel('occupancy (true nodes - false nodes)')
ax3.set_xlabel('step')
for t1 in ax3.get_yticklabels():
    t1.set_color('r')

ax4.plot( oval[1],'s')
ax4.set_ylabel('Output state ')
ax4.set_ylim([-.1,1.1])
ax4.set_yticks([0,1])
for t2 in ax4.get_yticklabels():
    t2.set_color('b')

ax5.plot(occup[2],'-',color='r',linewidth=4)
ax5.set_ylabel('occupancy (true nodes - false nodes)')
ax5.set_xlabel('step')
for t1 in ax5.get_yticklabels():
    t1.set_color('r')

ax6.plot( oval[2],'s')
ax6.set_ylabel('Output state ')
ax6.set_ylim([-.1,1.1])
ax6.set_yticks([0,1])
for t2 in ax6.get_yticklabels():
    t2.set_color('b')

ax7.plot(occup[3],'-',color='r',linewidth=4)
ax7.set_ylabel('occupancy (true nodes - false nodes)')
ax7.set_xlabel('step')
for t1 in ax7.get_yticklabels():
    t1.set_color('r')

ax8.plot( oval[3],'s')
ax8.set_ylabel('Output state ')
ax8.set_ylim([-.1,1.1])
ax8.set_yticks([0,1])
for t2 in ax8.get_yticklabels():
    t2.set_color('b')

f = P.gcf()
f.suptitle("512 OR fitness observed: "+str(fitness))
#f.set_size_inches(18,10)
#f.savefig('',dpi=100)
P.show()
