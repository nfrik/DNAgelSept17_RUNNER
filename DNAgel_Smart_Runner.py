__author__ = 'nfrik'

import os
import subprocess

root=os.getcwd();
working_dir = root+"/DNAgel_SEED"
executable = "networkgen_local.py"


# NODES = 2048
INPUTS = 2
OUTPUTS = 1
M = 30
ITERATIONS = 1
REPETITIONS = 1
TEST_AND = "test_and"
TEST_OR = "test_or"
TEST_XOR = "test_xor"
DISTR = "normal"
DISTRPAR1 = 15
DISTRPAR2 = 10

nodes=[32,64]

os.chdir(working_dir)
for node in nodes:
    subprocess.Popen(["python",executable,str(node),str(INPUTS),str(OUTPUTS),str(M),str(ITERATIONS),str(REPETITIONS),TEST_AND,DISTR,str(DISTRPAR1),str(DISTRPAR2)], stdout=subprocess.PIPE)
    subprocess.Popen(["python",executable,str(node),str(INPUTS),str(OUTPUTS),str(M),str(ITERATIONS),str(REPETITIONS),TEST_OR,DISTR,str(DISTRPAR1),str(DISTRPAR2)], stdout=subprocess.PIPE)
    subprocess.Popen(["python",executable,str(node),str(INPUTS),str(OUTPUTS),str(M),str(ITERATIONS),str(REPETITIONS),TEST_XOR,DISTR,str(DISTRPAR1),str(DISTRPAR2)], stdout=subprocess.PIPE)

# output, err = p.communicate()
# print err
# print output
print "*** Running nodes", nodes ," on ",  executable