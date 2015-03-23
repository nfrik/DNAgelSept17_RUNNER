import pydot
import networkx as nx
from functions import *
import random
import copy
import matplotlib.pyplot as plt
from pylab import *

global IDS;
IDS = 0  # singleton


class AbstractNode(object):
    def __init__(self, comment="", value=False):
        self.comment = comment
        self.value = value
        self.calculated_value = None


class IONode(AbstractNode):
    def __init__(self, ID, comment="", value=False, dump=False):
        AbstractNode.__init__(self, comment=comment, value=value)
        self.ID = ID

    def __repr__(self):
        return "< " + str(self.ID) + "<br/>State <b>" + str(self.value) + "</b>>"


class Node(AbstractNode):
    def __init__(self, function, comment="", value=False, dump=False):
        AbstractNode.__init__(self, comment=comment, value=value)
        self.func = function
        self.value = value
        self.comment = comment
        self.calculated_value = None

        global IDS
        self.ID = IDS
        IDS += 1

        if dump:
            print " * Node", IDS, "created with function", function, ", initial value", value

    def execute(self, params):
        try:
            return self.func(params)
        except:
            print "Unable to compute function (wrong arity?)"
            return None

    def set_output_value(self, val):
        self.value = val

    def __repr__(self):
        return "<Node <b>" + str(self.ID) + "</b><br/>Expression <b>" + str(
            self.func.implementation) + "</b><br/>State <b>" + str(self.value) + "</b>>"

    def calculate_function(self, params):
        # print "calculating function inside"
        self.calculated_value = self.func.apply(params)

    def apply_function(self):
        self.value = self.calculated_value


def load_truth_table_from_file(path):
    T = genfromtxt(path)
    rows = len(T)
    truth_table = {}
    with open(path) as fi:
        for i, riga in enumerate(fi):
            riga = riga.split()
            riga = map(lambda x: x == '1', riga)
            bitstring = binary_repr(i, width=int(log2(rows)))
            lista_input = []
            for bit in bitstring:
                lista_input.append(True if bit == '1' else False)
            truth_table[tuple(lista_input)] = riga
        return truth_table


class Network(object):
    def __init__(self):
        # print " * New emtpy network created"
        # IDS = 0		# sento che me ne pentiro'
        self.list_nodes = []
        self.list_functions = []
        self.list_directed_edges = {}
        self.max_arity = 0
        self.nodes_arities = {}
        self.input_nodes = []
        self.output_nodes = []
        self.truth_table = None
        self.graph_layout_pos = None

    def import_truth_table(self, path):
        self.truth_table = load_truth_table_from_file(path)


    def generate_random_functions(self, FUNCTIONS, max_depth=3):
        for funct in xrange(FUNCTIONS):
            rand_expr, expr_name, x_str, dt_ret = build_random_expression(
                list_operators=[("and", 2), ("or", 2), ("not", 1)], max_depth=max_depth)
            newcf = CustomFunction(expr_name, x_str)
            newcf.DT = dt_ret
            self.add_function(newcf, dump=False)

    def add_function(self, f, dump=False):
        if dump:
            print " * Function", f, "added to network"
        self.list_functions.append(f)
        if self.max_arity < f.arity:
            self.max_arity = f.arity
            print " * Maximum arity in network is now", self.max_arity
        try:
            a = self.nodes_arities[f.arity]
            self.nodes_arities[f.arity].append(f)
        except:
            self.nodes_arities[f.arity] = [f]
        if dump:
            print " * Functions with arity", f.arity, "are now", self.nodes_arities[f.arity]

    def add_node(self, n, dump=False):
        self.list_nodes.append(n)
        # self.add_function(n.func)
        if dump:
            print " * Node", n, "added"

    def add_directed_edge(self, start, end):
        # self.list_directed_edges.append([start, end])
        try:
            a = self.list_directed_edges[end]
            self.list_directed_edges[end].append(start)
        except:
            self.list_directed_edges[end] = [start]


    def update_states(self):
        for k in self.list_directed_edges:
            pars = []
            for n in self.list_directed_edges[k]:
                pars.append(n.value)
            k.calculate_function(pars)

        for k in self.list_directed_edges:
            k.apply_function()


    def calculate_nx_spring_layout(self):

        self.graph = nx.DiGraph()

        for i in self.input_nodes:
            self.graph.add_node(i.ID)

        for o in self.output_nodes:
            self.graph.add_node(o.ID)

        for f in self.list_nodes:
            self.graph.add_node(f.ID)

        for k in self.list_directed_edges:
            for num, n in enumerate(self.list_directed_edges[k]):
                self.graph.add_edge(n.ID, k.ID, label=n.ID)

        self.graph_layout_pos = nx.spring_layout(self.graph)


    def render_graph(self, p, boolean=True, use_networkx=False, use_png=False):
        if not use_networkx:
            self.generate_graph(boolean)
            if not use_png:
                self.graph.write(p)
            else:
                self.graph.write_png(p)
        else:
            colors = self.generate_graph_nx_colors(boolean)
            plt.figure(figsize=(20, 20))
            if self.graph_layout_pos != None:
                posit = nx.draw(self.graph, pos=self.graph_layout_pos, node_color=colors, font_size=7, node_size=300)
            else:
                posit = nx.draw_spring(self.graph, node_color=colors, font_size=7, node_size=300)
            plt.savefig(p)

    def generate_graph_nx_colors(self, boolean=True):

        self.graph = nx.DiGraph()

        colors = []

        # input nodes
        for i in self.input_nodes:
            self.graph.add_node(i.ID)
            if i.value == True:
                colors.append("lightgreen")
            else:
                colors.append("green")

        for o in self.output_nodes:
            self.graph.add_node(o.ID)
            if o.value == True:
                colors.append("brown")
            else:
                colors.append("red")

        for f in self.list_nodes:
            self.graph.add_node(f.ID)
            if f.value == True:
                colors.append('white')
            else:
                colors.append('gray')

        for k in self.list_directed_edges:
            for num, n in enumerate(self.list_directed_edges[k]):
                # print n.ID,"->",k.ID
                self.graph.add_edge(n.ID, k.ID, label=str(n.ID)+"->"+str(k.ID))

        return colors


    def get_number_from_nodeid(self, id):
        dict={}
        val=id
        base=10000000
        dict['I0']=base+0
        dict['I1']=base+1
        dict['I2']=base+2
        dict['I3']=base+3
        dict['I4']=base+4
        dict['I5']=base+5
        dict['I6']=base+6
        dict['O0']=base+7
        dict['O1']=base+8
        dict['O2']=base+9
        dict['O3']=base+10
        dict['O4']=base+11
        dict['O5']=base+12
        dict['O6']=base+13

        if id in dict.keys():
            val=dict[id]

        return val

    def generate_digraph_nx(self, boolean=True):

        G = nx.MultiGraph()

        edges = []

        for k in self.list_directed_edges:
            for num, n in enumerate(self.list_directed_edges[k]):
                # print n.ID,"->",k.ID
                # self.graph.add_edge(n.ID, k.ID, label=str(n.ID)+"->"+str(k.ID))
                edges.append((self.get_number_from_nodeid(n.ID),self.get_number_from_nodeid(k.ID)))

        G.add_edges_from(edges)
        # print edges
        return G

    def generate_graph_nx_labels(self, boolean=True):

        self.graph = nx.DiGraph()

        labels = {}
        # input nodes
        for i in self.input_nodes:
            self.graph.add_node(i.ID)
            labels[i.ID]="i"

        for o in self.output_nodes:
            self.graph.add_node(o.ID)
            labels[o.ID]="o"

        for f in self.list_nodes:
            self.graph.add_node(f.ID)
            labels[f.ID]=str(4)

        return labels

    def reset_network(self):
        for f in range(size(self.list_nodes)):
            self.list_nodes[f].value = False;
        for f in range(size(self.output_nodes)):
            self.output_nodes[f].value = False;


    def get_network_innter_state(self):
        lst = [-1] * size(self.list_nodes);
        for f in range(size(self.list_nodes)):
            if not self.list_nodes[f].value:
                lst[f] = 0
            else:
                lst[f] = 1
        return lst


    def get_body_states_occupancy(self):
        i = 0
        for f in range(size(self.list_nodes)):
            if self.list_nodes[f].value == True:
                i += 1
            else:
                i -= 1
        return i

    def evaluate_fitness(self):
        if self.truth_table == None:
            print "ERROR: no truth table specified"
            return 0
        else:
            target = []
            for i in self.input_nodes:
                target.append(i.value)
            tu = tuple(target)
            exp_output = self.truth_table[tu]
            for o1, o2 in zip(self.output_nodes, exp_output):
                # print o1.value, o2
                if o1.value != o2:
                    return False
        return True


    def generate_graph(self, boolean=True):
        # self.graph = pydot.Dot(splines="ortho")
        self.graph = pydot.Dot()

        # input nodes
        for n in self.input_nodes:
            fc = 'green'
            if boolean:
                if n.value == False:
                    fc = 'Aquamarine'
            self.graph.add_node(pydot.Node(str(n), shape="box", label=str(n), style='filled', fillcolor=fc))

        # output nodes
        for n in self.output_nodes:
            fc = 'brown'
            if boolean:
                if n.value == False:
                    fc = 'red'
            self.graph.add_node(pydot.Node(str(n), shape="box", label=str(n), style='filled', fillcolor=fc))

        for n in self.list_nodes:
            fc = 'white'
            if boolean:
                if n.value == False:
                    fc = 'gray'
            self.graph.add_node(pydot.Node(str(n), shape="box", label=str(n), style='filled', fillcolor=fc))
        for k in self.list_directed_edges:
            for num, n in enumerate(self.list_directed_edges[k]):
                pe = pydot.Edge(str(n), str(k))
                pe.set_label("<<sub>A" + str(num + 1) + "</sub>>")
                self.graph.add_edge(pe)


    def get_graph_degree(self):

        self.graph = nx.DiGraph()

        # input nodes
        for i in self.input_nodes:
            self.graph.add_node(i.ID)

        for o in self.output_nodes:
            self.graph.add_node(o.ID)

        for f in self.list_nodes:
            self.graph.add_node(f.ID)

        for k in self.list_directed_edges:
            for num, n in enumerate(self.list_directed_edges[k]):
                # print n.ID,"->",k.ID
                self.graph.add_edge(n.ID, k.ID, label=n.ID)

        return sorted(nx.degree(self.graph).values(), reverse=True);


    def get_connected_components_subgraphs(self):

        self.graph = nx.Graph()

        # input nodes
        for i in self.input_nodes:
            self.graph.add_node(i.ID)

        # output nodes
        for o in self.output_nodes:
            self.graph.add_node(o.ID)

        # core nodes
        for f in self.list_nodes:
            self.graph.add_node(f.ID)
            # print "Added node ",f.ID

        for k in self.list_directed_edges:
            for num, n in enumerate(self.list_directed_edges[k]):
                # print n.ID,"->",k.ID
                self.graph.add_edge(n.ID, k.ID, label=n.ID)

        ret = sorted(nx.connected_component_subgraphs(self.graph), reverse=True)[0];
        return ret

    def get_nx_digraph(self):

        self.graph = nx.DiGraph()

        # input nodes
        for i in self.input_nodes:
            self.graph.add_node(i.ID)

        # output nodes
        for o in self.output_nodes:
            self.graph.add_node(o.ID)

        # core nodes
        for f in self.list_nodes:
            self.graph.add_node(f.ID)
            # print "Added node ",f.ID

        for k in self.list_directed_edges:
            for num, n in enumerate(self.list_directed_edges[k]):
                # print n.ID,"->",k.ID
                self.graph.add_edge(n.ID, k.ID, label=n.ID)

        return self.graph

if __name__ == '__main__':

    net = Network()
    print net.generate_random_functions(100, max_depth=13)

    # ITERATIONS = 4
    # NODES = 30
    # FUNCTIONS = 20

    """
    cfand  = CustomFunction("AND", "A and B")
    cfnand = CustomFunction("NAND", "not (A and B)")
    cfnor  = CustomFunction("NOR", "not (A or B)")
    cfnot  = CustomFunction("NOT", "not A")
    cfor   = CustomFunction("OR", "A or B")
    cfxor  = CustomFunction("XOR", "A ^ B")
    """

    # set_of_functions = set()
    # for funct in xrange(FUNCTIONS):
    #     rand_expr, expr_name, x_str = build_random_expression(
    #         list_operators=[("and", 2), ("or", 2), ("not", 1), ("^", 2)], max_depth=3)
    #     newcf = CustomFunction(expr_name, x_str)
    #     set_of_functions.add(newcf)
    #
    # for x in xrange(NODES):
    #     rnd_fun = random.sample(set_of_functions, 1)[0]
    #     net.add_node(Node(rnd_fun, comment=str(rnd_fun), value=True))
    #
    # for selnode in net.list_nodes:
    #     # selnode = random.sample(net.list_nodes, 1)[0]
    #     # if selnode in net.list_directed_edges:
    #     # continue
    #
    #     all_nodes = net.list_nodes[:]
    #     a = selnode.func
    #     all_nodes.remove(selnode)
    #     nodes = random.sample(all_nodes, a.arity)
    #
    #     """
    #     nodes = []
    #     while(len(nodes)<a.arity) :
    #         n = random.sample(net.list_nodes, 1)[0]
    #         if n != selnode and n not in nodes:
    #             nodes.append(n)
    #     """
    #     for n in nodes:
    #         net.add_directed_edge(n, selnode)
    #
    #         # print "lista:" , net.list_directed_edges
    #
    # for i in xrange(ITERATIONS):
    #     print "Iteration", i
    #     net.render_graph("out" + str(i) + ".png")
    #     net.update_states()
