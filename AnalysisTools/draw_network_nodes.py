__author__ = 'nfrik'

import os
from numpy import *
import numpy
from scipy import integrate
import pylab as P
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time




def get_inner_states(path,repetition):
    ttab_cntr = 0
    ttab_max = 4
    stepStep = "Step: "
    stepInState = "InState: "
    repstr = "Repetition"
    outvalstr = "Output values:"
    statesoccup = "States occupancy:"
    fitstr = "Fitness for this run:"
    truth_table = "TRUTH_TABLE="
    states=[[[] for j in range(totIterations)] for i in range(ttab_max)]
    outvals=[[] for i in range(ttab_max)]
    iteration=0
    readnext = False
    with open(path) as f:
         for line in f:
            if (repstr in line) and (int(line.split()[2]) == repetition):
                readnext = True
            if readnext == True:
                if (stepStep in line) and (stepInState in line):
                    #oval[ttab_cntr]=eval(line.replace(stepStep," "))
                    states[ttab_cntr][iteration]=eval('['+line.split('[')[1])
                    iteration = iteration + 1

                if outvalstr in line:
                   outvals[ttab_cntr]=eval(line.replace(outvalstr," "))

                if statesoccup in line:
                       ttab_cntr+=1
                       iteration = 0

                if fitstr in line:
                   fitness = float(line.replace(fitstr," "))
                   ttab_cntr+=1
                if ttab_cntr == ttab_max+1:
                   break
    f.close()

    return states,outvals


REPETITION = 695
NODES = 64
TTROW =0

totIterations = 70
rootpath = "/Users/nfrik/Documents/DNAGelRuns/Research_RUNNER/"
filepath = rootpath+"DNAngel"+str(NODES)+"_XTRAtest_or/N"+str(NODES)+"_2_sample.log"

states,outvals = get_inner_states(filepath,REPETITION)
[states[TTROW][i].append(0.5*outvals[TTROW][i+1]) for i in range(totIterations)]


P.imshow(states[TTROW],interpolation='none',cmap='Blues')
# P.title("Inputs: "+"{0:b}".format(TTROW))

inputs = ["False True","True False","False False","True True"]
P.title("Inputs: " + str(inputs[TTROW]))
P.ylabel("Iteration")
P.xlabel("Nodes")
plt.show()
