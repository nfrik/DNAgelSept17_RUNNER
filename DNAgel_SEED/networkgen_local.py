__author__ = 'nfrik'
from nodes import *
from distributions import *
import sys
import datetime
import time
import os
import shutil
import matplotlib.pyplot as plt

def create_uniform_distribution(nodes, network, dump=True):
    dist = []
    initial_amount = nodes / (network.max_arity)
    residual_amount = nodes % (network.max_arity)
    if dump:
        print " * Max arity:", network.max_arity
        print network.nodes_arities
    for n in xrange(1, network.max_arity + 1):
        if n in network.nodes_arities.keys():
            dist.append(initial_amount)
        else:
            dist.append(0)
            residual_amount += initial_amount
    good_arities = len(network.nodes_arities.keys())
    conv_dict = list(network.nodes_arities)
    iva = 0
    while (residual_amount > 0):
        dist[conv_dict[iva] - 1] += 1
        residual_amount -= 1
        if iva < good_arities - 1:
            iva += 1
        else:
            iva = 0
    if dump:
        print " * Distribution of nodes:", dist
    return dist


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


# test network quality on random change of inputs
def iterate_network(net, TRUTH_TABLE, ITERATIONS, INPUTS, OUTPUTS, resultpath,reset_each_iteration):
    #resultpath = dirpath + "/rep_exceptional" + str(rho)
    GOOD = 0
    os.makedirs(resultpath)
    for line_n, line in enumerate(TRUTH_TABLE):

        for inp in xrange(INPUTS):
            net.input_nodes[inp].value = line[inp]

        for ou in xrange(OUTPUTS):
            net.output_nodes[ou].ID = "O" + str(ou)

        # net.calculate_nx_spring_layout()

        output_value  = []
        body_states_occupancy = []

        output_value.append(net.output_nodes[0].value)
        body_states_occupancy.append(1 if net.output_nodes[0].value==True else 0)

        for i in xrange(ITERATIONS[line_n]):
            #net.render_graph(resultpath + "/pdout" + str(line_n) + "_" + str(i) + ".dot", use_networkx=False, use_png=False)
            print "Step: ",i," InState: ", net.get_network_innter_state()
            net.update_states()

            if net.evaluate_fitness():
                GOOD += 1

                #check network quality

            output_value.append(1 if net.output_nodes[0].value==True else 0)
            body_states_occupancy.append(net.get_body_states_occupancy())

        print "Output values: ", output_value
        print "States occupancy: ", body_states_occupancy

        if reset_each_iteration:
            net.reset_network();

    # loc_fit = float(GOOD) / (len(net.truth_table) * sum(ITERATIONS))
    loc_fit = float(GOOD) / (sum(ITERATIONS))

    return loc_fit, output_value, body_states_occupancy

def plot_degree_histogram(net,par="",path=""):
    lst = net.get_graph_degree()
    # plt.plot(lst,'b-',marker='o')
    plt.loglog(lst,'b-',marker='o')
    plt.title("Degree rank plot for "+str(NODES)+" nodes"+par)
    plt.ylabel("degree")
    plt.xlabel("rank")

    plt.axes([0.45,0.45,0.45,0.45])
    Gcc=net.get_connected_components_subgraphs()
    # pos=nx.spring_layout(Gcc)
    pos=nx.circular_layout(Gcc)
    plt.axis('off')
    colors = net.generate_graph_nx_colors()
    nx.draw_networkx_nodes(Gcc,pos,node_size=40,node_color = colors)
    nx.draw_networkx_edges(Gcc,pos,alpha=0.4,width=1.3)
    plt.savefig(path+"/degree"+str(NODES)+".png")
    plt.show()

def plot_degree_histogram_manual(net,par="",path=""):
    data=[]
    for i in net.list_nodes:
        data.append(i.func.arity)

    # n, bins, patches = plt.hist(data, bins=20, facecolor='g', alpha=0.75)

    y,binEdges=np.histogram(data,bins=len(net.nodes_arities))
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    plt.plot(bincenters,y,'bo-')
    plt.title("Degree rank plot for "+str(NODES)+" nodes"+par)
    plt.ylabel("degree")
    plt.xlabel("rank")
    # plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    # plt.axis([40, 160, 0, 0.03])

    plt.axes([0.45,0.45,0.45,0.45])
    # Gcc=net.get_connected_components_subgraphs()
    # Gcc=net.get_nx_digraph()
    Gcc=net.generate_digraph_nx()
    # pos=nx.spring_layout(Gcc)
    pos=nx.circular_layout(Gcc)
    plt.axis('off')
    colors = net.generate_graph_nx_colors()
    nx.draw_networkx_nodes(Gcc,pos,node_size=1,node_color = colors, node_shape = 's', with_labels = False)
    nx.draw_networkx_edges(Gcc,pos,alpha=0.01,width=1.3)
    plt.savefig(path+"/degree"+str(NODES)+".png")
    plt.show()

def generate_distribution(d=None, distrib="", mu=10, sigma=5, lam=10, sf=100, normalization=10):
        if distrib == "uniform":
            d.initialize_uniform()
        elif distrib == "normal":
            d.initialize_normal(mu=mu,sigma=sigma)
        elif distrib == "poisson":
            d.initialize_poisson(lam=lam)
        elif distrib == "power_law":
            d.initialize_power_law(gamma=sf)

        d.normalize(toval = normalization)

if __name__ == '__main__':

    NODES = 1000
    INPUTS = 2
    OUTPUTS = 1
    M = 200
    ITERATIONS = 70
    REPETITIONS = 10
    TEST = "test_or"
    #NODES = int(sys.argv[1])
    #INPUTS = int(sys.argv[2])
    #OUTPUTS = int(sys.argv[3])
    #M = int(sys.argv[4])
    #ITERATIONS = int(sys.argv[5])
    #REPETITIONS = int(sys.argv[6])
    #TEST = sys.argv[7]
    #DISTRIBT = sys.argv[8]
    #DISTRARG1 = sys.argv[9]
    #DISTRARG2 = sys.argv[10]

    DISTRIBT = "normal"
    DISTRARG1 = 10
    DISTRARG2 = 4

    TRUTH_TABLE = load_truth_table_from_file(TEST)
    TOTAL_GOODS = 0
    REPETITION_GOODS = 0

    # append stuff into logger
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%m%d%Y_%H_%M_%S')
    dirpath = "/Users/nfrik/Documents/DELETEME_DISTRIBS_TEST/DNAgel" + str(NODES)+ timestamp + "_XTRA" + TEST
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    #sys.stdout = open(dirpath + "/N" + str(NODES) + "_2_sample.log", 'a')

    print '*************************************'
    print 'Timestamp: ', datetime.datetime.now()
    print 'NODES= ', NODES
    print 'INPUTS= ', INPUTS
    print 'OUTPUTS= ', OUTPUTS
    print 'M= ', M
    print 'ITERATINS= ', ITERATIONS
    print 'REPETITIONS= ', REPETITIONS
    print 'TRUTH_TABLE= ', TRUTH_TABLE
    print '*************************************'

    for rho in xrange(REPETITIONS):

        GOOD = 0

        print " * Repetition", rho, "*" * 50
        subresults = []

        net = Network()
        net.truth_table = TRUTH_TABLE

        # #Create Dummy I/O
        net.input_nodes = [];
        net.output_nodes = [];
        for inp in xrange(INPUTS):
            net.input_nodes.append(IONode("I" + str(inp)))
            net.input_nodes[-1].value = False

        for ou in xrange(OUTPUTS):
            net.output_nodes.append(Node(CustomFunction("ID1", "A")))
            net.output_nodes[-1].ID = "O" + str(ou)


        # Generates a set of random expressions
        # M - max cardinality
        # max_depth - tree depth
        net.generate_random_functions(M, max_depth=15)
        d = Distribution(bins=net.max_arity, tokens=NODES)

        generate_distribution(d=d,distrib=DISTRIBT,mu=DISTRARG1,sigma=DISTRARG2,lam=DISTRARG1,sf=DISTRARG1,normalization=NODES)

        # d.initialize_power_law(gamma=lambd)
        # d.normalize(toval=NODES)
        # d.initialize_normal(mu=mu,sigma=sigma,norm = 1*NODES)
        # d.initialize_uniform()
        # d.normalize(toval=1*NODES)
        # d.initialize_trunc_gauss(mu=mu, sigma=sigma)
        # d.initialize_normal(mu=mu,sigma=sigma,norm=1*NODES)
        # d.initialize_poisson(lam=20)
        # plot(range(1,len(d.amounts)+1),d.amounts,'ro-')

        d.filter_bins(net.nodes_arities)
        generate_random(net, NODES, generator=d)
        plot_degree_histogram_manual(net,DISTRIBT+" args = ("+str(DISTRARG1)+" , "+str(DISTRARG2)+")",path=dirpath)
        # net.render_graph(dirpath + "/pdout" + "_" + ".png", use_networkx=False, use_png=True)
        # print "resulted number of nodes:",size(net.list_nodes)
        # exit()
        # plot_degree_histogram(net," sigma="+sigma+" mu="+mu)


        resultpath = dirpath + "/rep" + str(rho)
        extra_resultpath = dirpath + "/rep_exceptional" + str(rho)
        #os.makedirs(resultpath)
        net.render_graph(dirpath + "/pdout" + "_" + ".dot", use_networkx=False, use_png=False)
        loc_fit, output_value, body_states_occupancy = iterate_network(net, TRUTH_TABLE, [ITERATIONS]*4, INPUTS, OUTPUTS,resultpath,reset_each_iteration=True);

        print "Fitness for this run: ", loc_fit

        if loc_fit >= 0.9:
            print "Network is exceptional, going for next step"
            #check network quality
            extra_iter = [20 + int(ITERATIONS * random.random()) for i in xrange(len(TRUTH_TABLE))]
            print "Extra_iterations: ", extra_iter
            loc_fit, output_value, body_states_occupancy = iterate_network(net, TRUTH_TABLE, extra_iter, INPUTS, OUTPUTS,extra_resultpath,reset_each_iteration=False)
            print "Extra exceptional table checkup fitness", loc_fit

        else:
            shutil.rmtree(resultpath)

    print "Fitness based on whole run:", float(REPETITION_GOODS) / (len(net.truth_table) * REPETITIONS * ITERATIONS)
    print "Total good circuits:", TOTAL_GOODS
    print 'Timestamp: ', datetime.datetime.now()