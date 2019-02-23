import networkx as nx 

CG = nx.complete_graph(4) 
PG = nx.path_graph(4) 
DG = nx.DiGraph([(0, 1), (1, 2), (0, 3), (3, 2)])

roots = DG.nodes
leaves = DG.nodes

all_paths = set()
for root in roots:
    for leaf in leaves:
        paths = nx.all_simple_paths(DG, root, leaf)
        for path in list(paths):
            path = tuple(path)
            all_paths.add(path)

print(all_paths)
