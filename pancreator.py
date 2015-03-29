__author__ = 'nfrik'

import string
import random
import datetime
import time
import os
import subprocess
import sys

def id_generator(size=3, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def datetimestamp():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%m%d%Y_%H_%M_%S')



N=[32,64,128,256,512,1024,1152,1280,1408,1536,1664,1792,1920,2048]
Rand=["False","True"]
M=[30,300]
Depth=[5,10,15,20]
Rep=[10]
Iter=[70]
TTable=["test_or","test_and","test_xor"]
d_key={1:"uniform",2:"normal",3:"poisson",4:"power_law"}
Inputs = 2
Outputs = 1
AllDists={1:[(0.,0.)],\
		  2:[(0.,0.)],\
		  3:[(0.,0.)],\
		  4:[(0.5,0.),(0.7,0.),(1.,0.),(1.2,0.),(1.5,0.),(1.7,0.),(2.,0.),(2.2,0.),(2.5,0.),(2.7,0.),(3.,0.),(3.2,0.),(3.5,0.),(3.7,0.),(4.,0.)]}
Jobs=3


# distrib number and param number
dis_n = 1
dis_p = 0
Distr=[d_key[dis_n],AllDists[dis_n]]


dirs = []
data = []
data.append({"N":N[0],"Inputs":Inputs,"Outputs":Outputs,"Rand":Rand[0],"M":M[1],"Depth":Depth[2],"Rep":Rep[0],"Iter":Iter[0],"TTable":TTable[0],"Distr":Distr,"TimesRep":1})
data.append({"N":N[1],"Inputs":Inputs,"Outputs":Outputs,"Rand":Rand[0],"M":M[1],"Depth":Depth[2],"Rep":Rep[0],"Iter":Iter[0],"TTable":TTable[0],"Distr":Distr,"TimesRep":2})
data.append({"N":N[1],"Inputs":Inputs,"Outputs":Outputs,"Rand":Rand[0],"M":M[1],"Depth":Depth[2],"Rep":Rep[0],"Iter":Iter[0],"TTable":TTable[0],"Distr":Distr,"TimesRep":2})

root=os.getcwd();


#for d in data:

	# print str(d["Distr"][0])
	#create dir
	# dirpath = root+"/RUN_" + datetimestamp() + "_ID_" + id_generator() + "_" + d["Distr"][0] + str(float(d["Distr"][1][0][0])) +"_"+ str(float(d["Distr"][1][0][1])) + "_N" + str(d["N"])
	# print dirpath
	# if not os.path.isdir(dirpath):
	# 	os.makedirs(dirpath)

	# #move to dir
	# os.chdir(dirpath)

njobs = 0
f = open("inputdata.txt",'w')
for line in data:
	for i in range(line["TimesRep"]):
		f.write(repr(line)+'\n')
		njobs+=1
f.close()

print "Jobs planned:", njobs

lsfscript = ("#!/bin/csh\n"
			   "#BSUB -n 4\n"
			   "#BSUB -R span[ptile=8]\n"
			   "#BSUB -W 24:00\n"
			   "#BSUB -J testArray[1-%(jobs)s]\n"
			   "#BSUB -o output.%%I\n"
			   "#BSUB -e error.%%I\n"
			   "#BSUB -u nvfrik@ncsu.edu\n"
			   "source /usr/local/apps/python/python276.csh\n"
		       "setenv PATH /usr/local/apps/graphviz/gnu32/2.18/bin:$PATH\n"
			   "python ./pytest.py %(params)s") % \
			    {'params':"$LSB_JOBINDEX",'jobs':njobs}

	# pytest = ("import sys\n"
	# 		  "data = eval(sys.argv[1])\n"
	# 		  'f = open("out.txt","w")\n'
	# 		  "f.write(repr(data.keys()))\n"
	# 		  "f.close()")
	
	# f = open("pytest.py",'w')
	# f.write(pytest)
	# f.close()
	# time.sleep(1)
	# subprocess.Popen(["python","pytest.py",repr(d)], stdout=subprocess.PIPE)

f = open("runscr.sh",'w')
f.write(lsfscript)
f.close

	# time.sleep(1)
	# subprocess.Popen(["bsub","<","runscr.sh"], stdout=subprocess.PIPE)
	
	#move back to root
	# os.chdir(root)
	# dirs.append(dirpath+"\n")
