__author__ = 'nfrik'

from dateutil import parser
import time

# strl = "Timestamp:"
#
#
# f=open("/Users/nfrik/Documents/Research_RUNNER/DNAngel8_XTRAtest_and/N8_2_sample.log")
# date=[]
# for line in f:
#     if strl in line:
#            date.append(parser.parse(line.replace(strl," ")))
#
# f.close()
#
# print date[1]-date[0]


strl = "Timestamp:"
rootpath = "/Users/nfrik/Documents/Research_RUNNER/"

data=[2048]
list=[[] for i in range(len(data))]

for i in range(len(data)):
    f=open(rootpath+"DNAngel"+str(data[i])+"_XTRAtest_and/N"+str(data[i])+"_2_sample.log")
    iter=0
    date0=0
    date1=0
    for line in f:
        if strl in line:
               if iter==0:
                   date0=parser.parse(line.replace(strl," "))
                   print date0
               elif iter==1:
                   date1=parser.parse(line.replace(strl," "))
                   print date1
               iter=iter+1

    a=time.mktime(time.strptime(str(date0),"%Y-%m-%d %H:%M:%S.%f"))
    b=time.mktime(time.strptime(str(date1),"%Y-%m-%d %H:%M:%S.%f"))
    list[i].append("%.2f" %  ((b-a)/3600.0))

    f.close()

print list