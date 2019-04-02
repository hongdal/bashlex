import networkx as nx 
from networkx.drawing import nx_pydot
import time 
import sys

"""
    netnodex is a wrapper of networkx graph. 

    self.graph is a MultiDiGraph class. 
    self.node_ids is a list of string. Each string is the NAME of the node in the .dot file. 
    self.graph.nodes['2'] is a dictionary. It is the data of the node. Usually it's the 
        { 'label' : '"xxx"'}
        Note, the double qoutes in the value is because the value of label in .dot file has double qoutes.


    There are three ways to create a new netnodex objet. 
    1. from a MultiDiGraph object.  If graph != None, ignore fname. 
    2. from a file. Only consider when graph == None
    3. create without initialization. Only when graph == None and fname == ''

"""


class netnodex:

    '''
        This class is a wrapper of networkx.classes.multidigraph.MultiDiGraph
        There are additional attributes used when computing the patterns. 

        nxgraph     :   the networkx.classes.multidigraph.MultiDiGraph 
        name        :   a unique name of the graph, usually this is the name of the bash file. 

    '''
    def __init__(self, graph=None, fname=""):
        if None != graph:
            self.graph = graph
            self.fname = ""
            self.node_ids = list(self.graph.nodes)
        elif "" != fname:
            self.fname = fname
            self.graph = nx_pydot.read_dot(fname)
            self.node_ids = list(self.graph.nodes)
        else:
            self.graph = None 
            self.fname = ""
            self.node_ids = None 
        self.node_hash = {}
        self.all_paths = set()


    def read_from_dot(self, fname):
        self.fname = fname
        self.graph = nx_pydot.read_dot(fname)
        self.node_ids = list(self.graph.nodes)


    def write_to_dot(self, fname):
        nx_pydot.write_dot(self.graph, fname)


    def write_subgraph_to_dot(self, subgraph, fname):
        nx_pydot.write_dot(subgraph, fname)


    def load_node_names(self):
        for node, v in self.graph.nodes(data='label'): 
            self.node_hash[node] = v


    def get_node_ids(self):
        return self.node_ids


    def get_node_data(self, nid):
        return self.graph.nodes[nid]


    def get_edge_view(self):
        return self.graph.edges


    def get_node_view(self):
        return self.graph.nodes


    # Generate all possible paths between every two nodes
    # This function returns a set of tuple. 
    # Each tuple is a path. 
    # Attention: This is very very time consuming. 
    # It may takes you 1000 years for 100s of nodes. 
    def compute_all_paths(self):
        self.all_paths = set()
        for source in self.graph.nodes:
            for target in self.graph.nodes:
                paths = nx.all_simple_paths(self.graph, source, target, cutoff=15)
                for path in list(paths):
                    path = tuple(path)
                    self.all_paths.add(path)
        return self.all_paths


    # This function returns a set of tuple. 
    # Each tuple in the set is a path. 
    # Attention, this is very time consuming. 
    # It may cause crash on a complex graph with 100s of nodes. 
    def get_start_to_end_paths(self):
        sources = set([])
        targets = set([])
        self.all_paths = set()
        # make all sources and targets. 
        for node in self.graph.nodes:
            if self.graph.in_degree(node) < 1:
                sources.add(node)
            if self.graph.out_degree(node) < 1:
                targets.add(node)
        # make all from-source-to-targets paths.
        for src in sources:
            for dst in targets:
                paths = nx.all_simple_paths(self.graph, src, dst)
                for path in list(paths):
                    path = tuple(path)
                    self.all_paths.add(path)
        return self.all_paths


    # Always call this function to get the paths.  
    # This function returns a set of tuple. 
    # Each tuple is a path (with human redable labels).
    def condense_all_paths(self):
        self.condensed_paths = set()
        for path in self.all_paths:
            list_path = list(path)
            for i in range(len(list_path)):
                list_path[i] = self.node_hash[list_path[i]]
            tuple_path = tuple(list_path)
            self.condensed_paths.add(tuple_path)                
        

    def get_path_with_length(self, shortest, longest):
        ret = set()
        for path in self.condensed_paths:
            if len(path) >= shortest and len(path) <= longest:
                ret.add(path) 
        return ret


    def print_paths(self, paths):
        for path in paths:
            print(path)



#infname = "../smallset/VirusShare_aaab8847a7c407b504d80dfc30b8f221.dot"
infname = "../smallset/VirusShare_aaab8847a7c407b504d80dfc30b8f221.small.dot"
#outfname = "../smallset/VirusShare_aaab8847a7c407b504d80dfc30b8f221-2.dot"

def test(shortest, longest):
    nd = netnodex()
    nd.read_from_dot(infname)
    nd.load_node_names()
    print("waiting...")
    # all_paths = nd.compute_all_paths()
    all_paths = nd.get_start_to_end_paths()
    nd.condense_all_paths()
    sp = nd.get_path_with_length(shortest,longest)
    nd.print_paths(sp)
    print("Number of nodes: %d" % len(nd.get_node_ids()))
    print("Number of edges: %d" % len(nd.get_edge_view()))
    print("Number of paths found: %d" % len(all_paths))
    print("Number of unique paths: %d" % len(nd.condensed_paths))
    print("Number of paths selected: %d" % len(sp))
    exit(0)
    #print(node_view(data='label'))
    #print(nd.get_node_data('2'))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: %s %s %s" % (sys.argv[0], "<shortest>", "<longest>"))
        exit(0)
    test(int(sys.argv[1]), int(sys.argv[2]))






