#!/usr/bin/env python

import os
import time
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import networkx as nx
from graph import Graph
from utils import plot_graph, get_common_subgraph

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
    # -----------------------------------------------general settings--------------------------------------------------
    parser.add_argument('--graph-format', default='adjlist', choices=['adjlist', 'edgelist'],
                        help='graph/network format')
    parser.add_argument('--graph-files', default='data/',
                        help='graph/network file')
    parser.add_argument('--attribute-file', default='data/cora_attr.txt',
                        help='node attribute/feature file')
    parser.add_argument('--label-file', default='data/cora_label.txt',
                        help='node label file') 
    parser.add_argument('--directed', default=True, action='store_true',
                        help='directed or undirected graph')                                               
    args = parser.parse_args()
    return args

def main(args):
    #g = Graph()  # see graph.py for commonly-used APIs and use g.G to access NetworkX APIs
    #print(f'Summary of all settings: {args}')

    # ---------------------------------------STEP1: load data-----------------------------------------------------
    #print('\nSTEP1: start loading data......')
    #t1 = time.time()
    # load graph structure info------
    graph_list = []
    count = 0
    if args.graph_format == 'adjlist':
        for adjlist in os.listdir(args.graph_files):
            if adjlist.endswith('adjlist'):
                graph_path = args.graph_files + adjlist
                g = Graph()
                g.read_adjlist(path=graph_path, directed=args.directed)
                graph_list.append(g)
                plot_graph(g.G, 'graph_'+str(count))
                print(adjlist)
                print("The num of nodes and edges of Graph %s : " % count, 
                      g.get_num_nodes(), g.get_num_edges())
                count += 1
                del g
    #elif args.graph_format == 'edgelist':
    #    g.read_edgelist(path=args.graph_file, weighted=args.weighted, directed=args.directed)

    for i in range(len(graph_list)-1):        
        for j in range(i+1, len(graph_list)):

            if (graph_list[i].get_num_nodes() < 14 and  graph_list[j].get_num_nodes() < 14):
                print(f'------ START @ {time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())} ------')       
                sim=graph_list[i].similarity_measure(graph_list[j])
                print("similarity between %s and %s: " % (i,j), sim)
                print(f'------ END @ {time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())} ------')

            common_subgraphs = get_common_subgraph(graph_list[i].G, graph_list[j].G)
            for k, graph in enumerate(common_subgraphs):
                plot_graph(graph, "%s_%s_%s"% (i, j, k))



if __name__ == '__main__':
    #print(f'------ START @ {time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())} ------')
    main(parse_args())
    #print(f'------ END @ {time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())} ------')