__author__ = 'nfrik'
from random import random
import random


# def expr(lst=[],depth=4):
#     if len(lst)>0 and depth>1:
#         a1=lst.pop()
#         a2=lst.pop()
#         # return '('+random.choice(['not ',' '])+str(a)+' '+expr(lst,depth-1)+')'
#         return '(' + str(a1) + expr(lst,depth-1) + random.choice(['and ','or ', 'not ']) + expr(lst,depth-1) + ')'
#     else:
#         return ""

# print expr(lst=['A1','A2','A3','A4'],depth=7)

def expr(lst,depth):

    #construct flat tree expression
    if len(lst)<=2:
        if len(lst)>1:
            return str(lst.pop()) + str(random.choice([' and ',' or '])) + str(lst.pop())
        elif len(lst)<2:
            return str(lst.pop())

    return '(' + random.choice([' not ','']) + expr(lst[:-1],depth-1) + random.choice([' and ',' or ']) + random.choice([' not ','']) + expr(lst[:-1],depth-1) + ')'


exp  = expr(['1','0','1'],4)
print exp,' ',eval(exp)

