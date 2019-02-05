import networkx as nx 


class PatternGraph:

    '''
        This class is a wrapper of networkx.classes.multidigraph.MultiDiGraph
        There are additional attributes used when computing the patterns. 

        nxgraph     :   the networkx.classes.multidigraph.MultiDiGraph 
        name        :   a unique name of the graph, usually this is the name of the bash file. 

    '''
    def __init__(self, nxgraph, name):
        self.nxgraph = nxgraph
        self.name = name


    def get_edges(self):
        return self.nxgraph.edges

    def get_nodes(self):
        return self.nxgraph.nodes

     




