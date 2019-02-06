import networkx as nx 
from networkx.drawing import nx_pydot


class PatternGraph:

    '''
        This class is a wrapper of networkx.classes.multidigraph.MultiDiGraph
        There are additional attributes used when computing the patterns. 

        nxgraph     :   the networkx.classes.multidigraph.MultiDiGraph 
        name        :   a unique name of the graph, usually this is the name of the bash file. 

    '''
    def __init__(self):
        self.graph = None
        self.fname = ""


    def load_file(self, fname):
        self.fname = fname
        self.graph = nx.Graph(nx_pydot.read_dot(fname))


    def get_edges(self):
        return self.graph.edges


    def get_nodes(self):
        return self.graph.nodes

    def get_nodes(self)



fname = "../testcase/VirusShare_aa91a02e32e0aa714d0832f4ef86fba6.dot"

def test():
    pg = PatternGraph()
    pg.load_file(fname)
    edges = pg.get_edges()
    nodes = pg.get_nodes()
    print(edges)
    print(nodes)

if __name__ == "__main__":
    test()






