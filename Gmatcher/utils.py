import networkx as nx
from networkx.drawing.nx_agraph import to_agraph 

def plot_graph(G, graph_name):
    A1 = to_agraph(G) 
    A1.layout('dot')                                                                 
    A1.draw('%s.png' % graph_name) 

# https://stackoverflow.com/questions/43108481/maximum-common-subgraph-in-a-directed-graph
def get_maximum_common_subgraph(G_source, G_new):
    matching_graph=nx.Graph()

    for n1,n2,attr in G_new.edges(data=True):
        if G_source.has_edge(n1,n2) :
            matching_graph.add_edge(n1,n2,weight=1)

    graphs = list(nx.connected_component_subgraphs(matching_graph))

    mcs_length = 0
    mcs_graph = nx.Graph()
    for i, graph in enumerate(graphs):

        if len(graph.nodes()) > mcs_length:
            mcs_length = len(graph.nodes())
            mcs_graph = graph

    return mcs_graph

def get_common_subgraph(G_source, G_new):
    matching_graph=nx.Graph()

    for n1,n2,attr in G_new.edges(data=True):
        if G_source.has_edge(n1,n2) :
            matching_graph.add_edge(n1,n2,weight=1)

    graphs = list(nx.connected_component_subgraphs(matching_graph))
    cs_graph = []
    for i, graph in enumerate(graphs):
        if len(graph.nodes()) > 2:
            di_subgraph = G_source.subgraph(graph.nodes())
            cs_graph.append(di_subgraph)    

    return cs_graph