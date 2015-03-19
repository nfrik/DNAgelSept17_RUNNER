__author__ = 'nfrik'
from itertools import izip
from graph_tool.all import *
from numpy.random import randint
from numpy.random import poisson
from random import random
import matplotlib.pyplot as plt
import random, string
from nodes import *
from distributions import *
import platform
import os


def load_from_net(net=Network()):
    G=Graph(directed=True);

    #Create vertex state
    vtx_state_prop = G.new_vertex_property("int")

    #Create edge state property
    edge_state_prop = G.new_edge_property("int")

    #Create vertex function property
    vtx_function_prop = G.new_vertex_property("string")

    #Create vertex type
    vtx_type_prop = G.new_vertex_property("string")

    #Create graph dictionary
    vertex_dictionary = G.new_graph_property("object")

    vtx_dict={}

    idx=0
    for b in net.list_nodes:
        vtx_dict[b.ID] = idx
        n=G.add_vertex()
        vtx_state_prop[n]= 1 if b.value == True else 0
        vtx_type_prop[n] = "R"
        idx+=1

    for b in net.input_nodes:
        vtx_dict[b.ID] = idx
        n=G.add_vertex()
        vtx_state_prop[n]= 1 if b.value == True else 0
        vtx_type_prop[n] = "I"
        idx+=1

    for b in net.output_nodes:
        vtx_dict[b.ID] = idx
        n=G.add_vertex()
        vtx_state_prop[n]= 1 if b.value == True else 0
        vtx_type_prop[n] = "O"
        idx+=1

    # #Connect network
    for k in net.list_directed_edges:
        vtx_function_prop[G.vertex(vtx_dict.get(k.ID))] = k.func.implementation
        for num,n in enumerate(net.list_directed_edges[k]):
            G.add_edge(G.vertex(vtx_dict.get(n.ID)),G.vertex(vtx_dict.get(k.ID)))
            # print n.ID,"->",k.ID

    #Set edge state from vertex state
    for v in G.vertices():
        for e in v.out_edges():
            edge_state_prop[e]=vtx_state_prop[v]

    G.vertex_properties["state"] = vtx_state_prop
    G.vertex_properties["type"] = vtx_type_prop
    G.vertex_properties["function"] = vtx_function_prop
    G.edge_properties["state"] = edge_state_prop
    G.graph_properties["dict"] = vertex_dictionary #sets map
    G.graph_properties["dict"] = vtx_dict #sets value

    return G

def generate_random_net(N,INPUTS,OUTPUTS,random_state=False):

    #distribution function to be replaced
    def deg_sample():
        if random.random() < 0.5:
            return poisson(3) + 1 , poisson(3) + 1
        else:
            return poisson(16) + 1 , poisson(16) + 1

    G=random_graph(N,deg_sample,directed=True)

    print "Random graph generated with ",N," nodes"

    #Create vertex state
    vtx_state_prop = G.new_vertex_property("int")

    #Create edge state property
    edge_state_prop = G.new_edge_property("int")

    #Create vertex function property
    vtx_function_prop = G.new_vertex_property("string")

    #Create vertex type
    vtx_type_prop = G.new_vertex_property("string")

    vtx_dict={}

    reg_vtx=[];
    inp_vtx=[];
    out_vtx=[];

    idx=0

    for v in G.vertices():
        vtx_state_prop[v] = 0 if not random_state else random.randint(0,1)
        vtx_type_prop[v] = "R"
        # vtx_function_prop[v] = expr(["A"+str(i) for i in range(1,v.in_degree()+1)])
        idx+=1
    print "Network vertices type assigned"


    for i in range(INPUTS):
        iv = G.add_vertex()
        #G.add_edge(iv,G.vertex(random.randint(0,N)))
        vtx_state_prop[iv] = 0
        vtx_type_prop[iv] = "I"
        idx+=1
    print "Input vertices type assigned"

    for o in range(OUTPUTS):
        ov = G.add_vertex()
        # G.add_edge(G.vertex(random.randint(0,N)),ov)
        vtx_state_prop[ov] = 0 if not random_state else random.randint(0,1)
        vtx_type_prop[ov] = "O"
        idx+=1
    print "Output vertices type assigned"

    #connect inputs and outputs and assign funcitons to core vertices

    for v in G.vertices():
        if vtx_type_prop[v] == "I":
            inp_vtx.append(v)
        elif vtx_type_prop[v] == "O":
            out_vtx.append(v)
        elif vtx_type_prop[v] == "R":
            reg_vtx.append(v)

    G.vertex_properties["state"] = vtx_state_prop
    G.vertex_properties["type"] = vtx_type_prop
    G.vertex_properties["function"] = vtx_function_prop
    G.edge_properties["state"] = edge_state_prop
    # G.graph_properties["dict"] = vtx_dict #sets value

    pos = arf_layout(G,max_iter=0)
    for iv in inp_vtx:
        ed=G.add_edge(iv,random.sample(reg_vtx,1)[0])
        # graph_draw(G,pos=pos,vertex_fill_color=vtx_color(G),output="sample.png")

    print "Input nodes assigned"

    for ov in out_vtx:
        ed=G.add_edge(random.sample(reg_vtx,1)[0],ov)
    print "Output nodes assigned"

    for rv in reg_vtx:
        # print rv.in_degree()+1,vtx_type_prop[rv],["A"+str(i) for i in range(1,rv.in_degree()+1)]
        vtx_function_prop[rv] = expr(["A"+str(i) for i in range(1,rv.in_degree()+1)])
    print "Node functions assigned"

    G.vertex_properties["state"] = vtx_state_prop
    G.vertex_properties["type"] = vtx_type_prop
    G.vertex_properties["function"] = vtx_function_prop
    G.edge_properties["state"] = edge_state_prop
    # G.graph_properties["dict"] = vtx_dict #sets value

    return G

def expr(lst):

    #construct flat tree expression
    if len(lst)<=2:
        if len(lst)>1:
            return str(lst.pop()) + str(random.choice([' and ',' or '])) + str(lst.pop())
        elif len(lst)==1:
            return str(lst.pop())
        elif len(lst)==0:
            return

    return '(' + random.choice([' not ','']) + expr(lst[:-1]) + random.choice([' and ',' or ']) + random.choice([' not ','']) + expr(lst[:-1]) + ')'

def evolve(G):

    fprop = G.vp["function"]
    estate = G.ep["state"]
    vstate = G.vp["state"]
    vtype = G.vp["type"]


    # for v in G.vertices():
    #     if vtype[v]=="R":
    #         funct = fprop[v]
    #         for i,e in enumerate(v.in_edges()):
    #             print estate[e],
    #             funct = funct.replace('A'+str(i+1),str(estate[e]))
    #         else:
    #             print "->",funct,"->",eval(funct)


    #Update vertexes
    for v in G.vertices():
        if vtype[v]=="R": #Regular
            funct = fprop[v]
            for i,e in enumerate(v.in_edges()):
                funct = funct.replace('A'+str(i+1),str(estate[e])) #Ie replace 'A1' with 1st input node value

            vstate[v]=eval(funct)

            #Update output edges
            for e in v.out_edges():
                estate[e]=vstate[v]


    #Update output vertexes
    for v in G.vertices():
        if vtype[v]=="O": #Output
            for e in v.in_edges():
                vstate[v]=estate[e]
                print vstate[v],estate[e]


def vtx_color(G):
    vtx_color_property = G.new_vertex_property("int")
    vtype = G.vp["type"]
    vstate = G.vp["state"]
    for v in G.vertices():
        if vtype[v] == "R":
            vtx_color_property[v]=vstate[v]
        elif vtype[v] == "I":
            vtx_color_property[v]=vstate[v]+3
        elif vtype[v] == "O":
            vtx_color_property[v]=vstate[v]+6

    return vtx_color_property

def iterate_net():
    return 0

def generate_random(network, nodes, generator=None, dump=True, P=0.1):
    # for each possible degree, use frequency to
    # add new nodes
    degree_distribution = generator.amounts

    # dist = generator.array_of_samples(nodes)
    # print dist

    # per ogni elemento della distribuzione
    for d, freq in enumerate(generator.amounts):
        for i in xrange(int(freq)):
            rand_fun = random.sample(network.nodes_arities[d + 1], 1)[0]
            no = Node(rand_fun)
            network.add_node(no)

    for selnode in network.list_nodes:
        nodes = []

        all_nodes = network.list_nodes[:]
        all_nodes.remove(selnode)
        a = selnode.func

        while (len(nodes) < a.arity):

            if random.random() > P:
                inp_node = random.sample(all_nodes, 1)[0]
            else:
                # use inputs
                inp_node = random.sample(network.input_nodes, 1)[0]
            # print " * Selected input", inp_node
            nodes.append(inp_node)

        for n in nodes:
            net.add_directed_edge(n, selnode)

    for o in network.output_nodes:
        inp_node = random.sample(network.list_nodes, 1)[0]
        net.add_directed_edge(inp_node, o)

    print " * Generation completed"

if __name__ == '__main__':


    print "Hola!"
    print platform.python_version()
    NODES = 128
    INPUTS = 2
    OUTPUTS = 1
    M = 100
    ITERATIONS = 70
    REPETITIONS = 150
    TEST = "test_or"
    # NODES = int(sys.argv[1])
    # INPUTS = int(sys.argv[2])
    # OUTPUTS = int(sys.argv[3])
    # M = int(sys.argv[4])
    # ITERATIONS = int(sys.argv[5])
    # REPETITIONS = int(sys.argv[6])
    # TEST = sys.argv[7]

    TRUTH_TABLE = load_truth_table_from_file(TEST)
    TOTAL_GOODS = 0
    REPETITION_GOODS = 0

    # net = Network()
    # net.truth_table = TRUTH_TABLE
    #
    # # #Create Dummy I/O
    # net.input_nodes = [];
    # net.output_nodes = [];
    #
    # for inp in xrange(INPUTS):
    #     net.input_nodes.append(IONode("I" + str(inp)))
    #     net.input_nodes[-1].value = True
    #
    # for ou in xrange(OUTPUTS):
    #     net.output_nodes.append(Node(CustomFunction("ID1", "A")))
    #     net.output_nodes[-1].ID = "O" + str(ou)
    #
    #
    # # Generates a set of random expressions
    # # M - max cardinality
    # # max_depth - tree depth
    # net.generate_random_functions(M, max_depth=3)
    # d = Distribution(bins=net.max_arity, tokens=NODES)
    # d.initialize_uniform()
    # d.filter_bins(net.nodes_arities)
    # generate_random(net, NODES, generator=d)
    #
    # G = load_from_net(net);


    path="/picsRand"
    if not os.path.isdir("."+path):
        os.makedirs("."+path)


    G=generate_random_net(NODES,2,1,random_state=False)
    pos = arf_layout(G,max_iter=0)
    # for i in range(10):
    #     graph_draw(G,pos=pos,vertex_fill_color=vtx_color(G),output="picsRand/sample"+str(i)+".png")
    #     evolve(G)



    # pos = arf_layout(G,max_iter=0)
    # graph_draw(G,pos=pos,vertex_fill_color=vtx_color(G),output="sample.png")



    in_hist = vertex_hist(G,"in")

    y=in_hist[0]
    err = sqrt(in_hist[0])
    err[err >= y] = y[err >= y] - 1e-2


    plt.figure(figsize=(6,4))
    errorbar(in_hist[1][:-1], in_hist[0], fmt="o", yerr=err,label="in")
    # gca().set_yscale("log")
    # gca().set_xscale("log")
    # gca().set_ylim(1e-1, 1e5)
    # gca().set_xlim(0.8, 1e3)
    subplots_adjust(left=0.2, bottom=0.2)
    xlabel("$k_{in}$")
    ylabel("$NP(k_{in})$")
    plt.show()


    # for i in range(100):
    #     graph_draw(G,pos=pos,vertex_fill_color=vtx_color(G),output="pics2/sample"+str(i)+".png")
    #     evolve(G)