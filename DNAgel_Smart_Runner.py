__author__ = 'nfrik'

import os
import subprocess

root=os.getcwd();
working_dir = root+"/DNAgel_SEED"
executable = "networkgen.py"


# NODES = 2048
INPUTS = 2
OUTPUTS = 1
M = 30
ITERATIONS = 70
REPETITIONS = 1024
TEST_AND = "test_and"
TEST_OR = "test_or"
TEST_XOR = "test_xor"

nodes=[32]

os.chdir(working_dir)
for node in nodes:
    subprocess.Popen(["python",executable,str(node),str(INPUTS),str(OUTPUTS),str(M),str(ITERATIONS),str(REPETITIONS),TEST_AND], stdout=subprocess.PIPE)
    subprocess.Popen(["python",executable,str(node),str(INPUTS),str(OUTPUTS),str(M),str(ITERATIONS),str(REPETITIONS),TEST_OR], stdout=subprocess.PIPE)
    subprocess.Popen(["python",executable,str(node),str(INPUTS),str(OUTPUTS),str(M),str(ITERATIONS),str(REPETITIONS),TEST_XOR], stdout=subprocess.PIPE)

# output, err = p.communicate()
# print err
# print output
print "*** Running nodes", nodes ," on ",  executable