__author__ = 'nfrik'
from itertools import izip
from graph_tool.all import *
from numpy.random import randint
from numpy.random import poisson
from random import random
import matplotlib.pyplot as plt
import random, string
import platform

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


def sample_k(max):
     accept = False
     while not accept:
         k = randint(1,max+1)
         accept = random() < 1.0/k
     return k


# g=random_graph(1000, lambda: sample_k(40), model="probabilistic",vertex_corr=lambda i, k: 1.0 / (1 + abs(i - k)), directed=False,n_iter=100)
# hist = combined_corr_hist(g,"in","out")

g=random_graph(100,lambda: (poisson(3), poisson(3)),edge_sweep=False,random=False,self_loops=True,verbose=False,persist=False)

vformula = g.new_vertex_property("string")
vformularr = g.new_vertex_property("vector<int>")
edgelabel = g.new_edge_property("string")
edgestate = g.new_edge_property("int")
for v in g.vertices():
    vformula[v]=randomword(randint(2,5))
    vformularr[v]=[random.randint(0,10) for i in range(v.out_degree())]
    i=1
    for e in v.out_edges():
        edgelabel[e]=str(i)
        i=i+1




g.vertex_properties["formula"] = vformula
g.vertex_properties["vector"] = vformularr
g.edge_properties["edgelabel"] = edgelabel

g.save("save.gt")
g2 = load_graph("save.gt")


indeg=0; outdeg=0
for v in g2.vertices():
    print "Out deg", v.out_degree(), " In deg: ", v.in_degree()
    indeg+=v.in_degree();
    outdeg+=v.out_degree();
print "Out deg tot ", outdeg, " In deg tot: ", indeg

pr = g2.vp["formula"]
# for vertex in g2.vertices():
#     print pr[vertex]

el = g2.ep["edgelabel"]
# for edge in g2.edges():
#     print el[edge]

print platform.python_version()

pos = sfdp_layout(g2,K=0.1)
graph_draw(g2,pos=pos,vertex_text=pr,edge_text = el,output="/Users/nfrik/Dropbox/Research/LaBean/DNAgelSept17_RUNNER/sample.png")



# plt.hist(out_hist[0])
#
# plt.show()

# # Playing with simple graph generation and saving
# g = Graph(directed=True)
#
# N=100
# g.add_vertex(N)
#
# vprop_label = g.new_vertex_property("string")
# vprop_shape = g.new_vertex_property("string")
# for s,t in izip(randint(0,N,N),randint(0,N,N)):
#     g.add_edge(g.vertex(s),g.vertex(t))
#     vprop_shape[g.vertex(s)]="square"
#     #vprop_label[g.vertex(s)] = str(0)
#
#
# # g.vertex_properties["labels"]=vprop_label
# g.vertex_properties["shape"]=vprop_shape
# g.save("graph.gt")
# g2=load_graph("graph.gt")
#
# g2.list_properties()
# graph_draw(g2,vprops={"shape":"square"},output="/Users/nfrik/Dropbox/Research/LaBean/DNAgelSept17_RUNNER/sample.png")
