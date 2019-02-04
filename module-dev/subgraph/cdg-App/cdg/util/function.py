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

    #graphs = list(nx.connected_component_subgraphs(matching_graph))
    graphs = list(matching_graph.subgraph(c) for c in nx.connected_components(matching_graph))

    cs_graph = []
    for i, graph in enumerate(graphs):
        di_subgraph = G_source.subgraph(graph.nodes())
        G_new_subgraph = G_new.subgraph(graph.nodes())
        if nx.number_of_edges(G_new_subgraph) < nx.number_of_edges(di_subgraph):
            di_subgraph = G_new_subgraph
        cs_graph.append(di_subgraph)    

    return cs_graph

# https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3
def hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, 
                  pos = None, parent = None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(G.neighbors(root)) 
    if parent != None:   #this should be removed for directed graphs.
        neighbors.remove(parent)  #if directed, then parent not in neighbors.
    if len(neighbors)!=0:
        dx = width/len(neighbors) 
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap, 
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, 
                                parent = root)
    return pos