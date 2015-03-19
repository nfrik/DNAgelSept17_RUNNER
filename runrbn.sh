#!/bin/csh
#BSUB -n 1
#BSUB -W 14
#BSUB -J testArray[1-1]
#BSUB -o out.%I
#BSUB -e err.%I
#BSUB -u nvfrik@ncsu.edu

source /usr/local/apps/python/python276.csh
setenv PATH /usr/local/apps/graphviz/gnu32/2.18/bin:$PATH
python ./DNAgel_Smart_Runner.py $LSB_JOBINDEX