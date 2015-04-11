__author__ = 'nfrik'
from parse import *
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import statsmodels.api as sm


root="/Users/nfrik/Documents/DNAGelRuns/"

file = root+ "output-5-2015-unif.txt";


# d={"N":[1,2]}
# d["N"].append(4)
# print d

# parse('./output/RUN_T{}_{}_{}_{}_{}_power_law{}_{}_N{}_{}_{}_R{}_M{}_D{:d}{}','./output/RUN_T03302015_04_48_02_261892_power_law4.0_0.0_N512_XTRAtest_xor_RTrue_M300_D8/graph_spring512_r_9.png')

r=[]

N256and=[]
N256or=[]
N256xor=[]
N512and=[]
N5126or=[]
N512xor=[]
N1024and=[]
N1024or=[]
N1024xor=[]

dic={"256":{"and":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]},"or":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]},"xor":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]}},\
     "512":{"and":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]},"or":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]},"xor":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]}},\
    "1024":{"and":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]},"or":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]},"xor":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]}},\
    "2048":{"and":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]},"or":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]},"xor":{"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]}}}

tabledic={"NN":[],"TT":[],"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]}
tmpdic={"NN":[],"TT":[],"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]}

Nidx=7
Lamidx=5
Tabidx=9
Midx=11
Didx=12
Runidx=13
Ti1=13
Ti2=14
Ti3=15

# dic["256"]["and"]["D"].append(5)

luid=0
i=0
with open(file) as f:
    for line in f:

        # r=parse('./output/RUN_T{}_{}_{}_{}_{}_power_law{}_{}_N{}_{}_{}_R{}_M{}_D{:d}/rep_exceptional{:d}{}',line)
        r=parse('./outputnorm/RUN_T{}_{}_{}_{}_{}_uniform{}_{}_N{}_{}_{}_R{}_M{}_D{:d}/{}',line)

        if r:
            rex=parse('rep_exceptional{:d}{}',r[Ti1])
            rpng=parse('graph_circ{:d}{}',r[Ti1])


        if r and (rex or rpng):
            if i==0:
                luid=''.join([r[0],r[1],r[2],r[3],r[4]])

            cuid=''.join([r[0],r[1],r[2],r[3],r[4]])

            if cuid!=luid:
                luid=cuid;

                #filter and append stuff from tmpdic to
                totex={0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
                for j in range(len(tmpdic["SUC"])):
                    #gather all exceptionals
                    tr=parse('rep_exceptional{:d}{}',tmpdic["SUC"][j])
                    if tr:
                        totex[tr[0]]=1

                for k in totex.keys():
                    if k < len(tmpdic["NN"]):
                        tabledic["NN"].append(tmpdic["NN"][k])
                        tabledic["TT"].append(tmpdic["TT"][k])
                        tabledic["D"].append(tmpdic["D"][k])
                        tabledic["M"].append(tmpdic["M"][k])
                        tabledic["LAM"].append(tmpdic["LAM"][k])
                        tabledic["SUC"].append(totex[k])

                tmpdic={"NN":[],"TT":[],"D":[],"M":[],"LAM":[],"RUN":[],"SUC":[]}

            # rr=parse('rep_exceptional{:d}{}',r[Tailidx])
            tmpdic["NN"].append(r[Nidx])
            tmpdic["TT"].append(r[Tabidx])
            tmpdic["D"].append(r[Didx])
            tmpdic["M"].append(r[Midx])
            tmpdic["LAM"].append(r[Lamidx])
            tmpdic["SUC"].append(r[Ti1])

            print i
            i+=1


            # if i>10:
            #      break;

        # if r:
        #     dic[r[Nidx]][r[Tabidx]]["D"].append(r[Didx])
        #     dic[r[Nidx]][r[Tabidx]]["M"].append(r[Midx])
        #     dic[r[Nidx]][r[Tabidx]]["LAM"].append(r[Lamidx])
        #     # dic[r[Nidx]][r[Tabidx]]["RUN"].append(r[Runidx])
        #     print r

        # r[Didx]
        # dic[r[Nidx]][Tabidx][Midx]=r[Midx]
        # dic[r[Nidx]][Tabidx][Midx]=r[Midx]

        # if r:
        # print r
        # if i>100:
        #      break;
        # i+=1


# print tabledic


f = open(root+"tabular_unif.txt",'w')
f.write(repr(tabledic))
f.close()

f = open(root+"tabular_unif.txt",'r')
# f.write(repr(tabledic))
tab = eval(f.read())
f.close()

f=open(root+"tabular_unif_tab_and.txt",'w')
for i in range(len(tab["SUC"])):
    if tab["TT"][i]=="and":
        f.write('\t'.join([str(tab["NN"][i]),str(tab["D"][i]),str(tab["M"][i]),str(tab["LAM"][i]),str(tab["SUC"][i]),'\n']))
f.close()

f=open(root+"tabular_unif_tab_or.txt",'w')
for i in range(len(tab["SUC"])):
    if tab["TT"][i]=="or":
        f.write('\t'.join([str(tab["NN"][i]),str(tab["D"][i]),str(tab["M"][i]),str(tab["LAM"][i]),str(tab["SUC"][i]),'\n']))
f.close()

f=open(root+"tabular_unif_tab_xor.txt",'w')
for i in range(len(tab["SUC"])):
    if tab["TT"][i]=="xor":
        f.write('\t'.join([str(tab["NN"][i]),str(tab["D"][i]),str(tab["M"][i]),str(tab["LAM"][i]),str(tab["SUC"][i]),'\n']))
f.close()

# f = open(root+"exceptional-full-checksum.txt",'r')
# diccheck = eval(f.read())
# f.close()
#
# # f = open(root+"exceptional.txt",'r')
# # dic = eval(f.read())
# # f.close()
#
f = open(root+"exceptional-full.txt",'r')
dicfull = eval(f.read())
f.close()
#
#
# f = open("excelfriendly.txt",'w')
# for NN in ["256","512","1024","2048"]:
#     for i in range(len(diccheck[NN]["xor"]["LAM"])):
#         if len(dicfull[NN]["xor"]["LAM"])
# f.close()






#
# PN=512
# PT="or"
# n,bins,patches = plt.hist([float(x) for x in dic["512"]["or"]['LAM']],normed=1,facecolor='blue',alpha=0.75)
# plt.title("")
# plt.show()


# print len(dic["256"]['xor']['LAM'])
# print len(dic["512"]['xor']['LAM'])
# print len(dic["1024"]['xor']['LAM'])
# print len(dic["2048"]['and']['LAM'])
#
# print "\n"
#
print len(dicfull["256"]['and']['LAM'])+len(dicfull["512"]['and']['LAM'])+len(dicfull["1024"]['and']['LAM'])+len(dicfull["2048"]['and']['LAM'])
print tab["SUC"][:].count(1)
# print len(dicfull["512"]['and']['LAM'])
# print len(dicfull["1024"]['and']['LAM'])
# print len(dicfull["2048"]['and']['LAM'])


# f = open("excelfriendly.txt",'w')
# for NN in ["256","512","1024","2048"]:
#     for i in range(len(dicfull[NN]["xor"]["LAM"])):
#         f.write('\t'.join(['xor',NN,str(dicfull[NN]["xor"]["D"][i]),str(dicfull[NN]["xor"]["M"][i]),str(dicfull[NN]["xor"]["LAM"][i]),'\n']))
# f.close()