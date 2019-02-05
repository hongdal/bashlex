# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Description:
# ---------
# Setup the datasets.
#
# --------------------------------------------------------------------------------
# Copyright (c) 2017-2018, Daniele Zambon
# All rights reserved.
# Licence: BSD-3-Clause
# --------------------------------------------------------------------------------
# Author: Daniele Zambon 
# Affiliation: Università della Svizzera italiana
# eMail: daniele.zambon@usi.ch
last_update = '24/05/2018'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import sys
import argparse
import cdg
import cdg.util.logger
import cdg.embedding.embedding
import cdg.embedding.manifold
import cdg.embedding.feature
import cdg.graph.database
import cdg.simulation.parameters
import cdg.graph.graph
import datetime
import networkx as nx
import numpy as np
from PatternExtractor import PatternGraph

from cdg.util.function import plot_graph, get_common_subgraph, hierarchy_pos
###############################################################################
# Edit this part
###############################################################################





# Set the debugging options
cdg.util.logger.set_stdout_level(cdg.util.logger.INFO)
log_file = cdg.util.logger.set_filelog_level(
    level=cdg.util.logger.DEBUG,
    name=datetime.datetime.now().strftime('%G%m%d%H%M-%f'))
cdg.util.logger.enable_logrun(level=False)


# Defines the datasets location
def get_elements_script(elements):
    #return elements['0'], elements['0'] + elements['2'] + elements['4'] + elements['6'] \
    #                                    + elements['8'] + elements['10'] + elements['11']
    return elements['0'], elements['0'] + elements['2'] + elements['4'] + elements['6'] \
                                        + elements['8']                                   


def get_elements_markov(elements):
    return elements['0'], elements['0'] + elements['1']

def get_elements_letter(elements):
    return elements['A'] + elements['E'] + elements['F'] + elements['H'] + elements['I'], \
           elements['A'] + elements['E'] + elements['F'] + elements['H'] + elements['I'] \
           + elements['K'] + elements['L'] + elements['M'] + elements['N'] + elements['T']

def get_elements_mutag(elements):
    return elements['nonmutagen'], elements['nonmutagen'] + elements['mutagen']

def get_elements_aids(elements):
    return elements['i'], elements['i'] + elements['a']

def get_elements_dog(elements):
    return elements['0'], elements['0'] + elements['1']


# gmt_executable = "./graph-matching-toolkit/graph-matching-toolkit.jar"

###############################################################################
# You are not supposed to edit this part
###############################################################################

# Available options for the arguments
# -----------------------------------

# Datasets
_use_gmt = True
_class_index = 0
_get_elements_index = 1
_use_gmt_index = 2
LETTER = ('Letter', cdg.graph.database.Letter, get_elements_letter, _use_gmt)
MUTAGENICITY = ('Mutagenicity', cdg.graph.database.Mutagenicity, get_elements_mutag, _use_gmt)
AIDS = ('AIDS', cdg.graph.database.AIDS, get_elements_aids, _use_gmt)
Script = ('Script', cdg.graph.database.Script, get_elements_script, _use_gmt)

MARKOV = ('Markov', cdg.graph.database.Markov, get_elements_markov, _use_gmt)
KAGGLEDOG = ('Kaggle', cdg.graph.database.KaggleSeizureDog, get_elements_dog, not _use_gmt)
_datasets = [LETTER, MUTAGENICITY, AIDS, Script, MARKOV, KAGGLEDOG]
available_datasets = {}
for _set in _datasets:
    available_datasets[_set[0]] = _set[1:]

# Define the argument parser
parser = argparse.ArgumentParser(description='')
# parser.add_argument('-e', '--experiment', type=str, help='experiment name')
parser.add_argument('-d', '--dataset', type=str, default='Script',
                    choices=available_datasets.keys(),
                    help='dataset name')
parser.add_argument('-p', '--data-path', type=str, default='../smallset',
                    help='path of the dataset')
parser.add_argument('-t', '--tmp-path', type=str, default='/tmp/bash',
                    help='path of the dataset')
parser.add_argument('-s', '--subdataset', type=str, default=None,
                    help='sometimes is needed')
parser.add_argument('-j', '--noJobs', type=int, default=-1,
                    help='number of jobs of joblib')
parser.add_argument('-c', '--classes', type=str, default='0',
                    help='delimited list input', )

cdg_path = os.path.dirname(os.path.realpath(__file__))
parser.add_argument('--gmtpath', type=str,
                    default=cdg_path+"/graph-matching-toolkit/graph-matching-toolkit.jar",
                    help='path to the graph matching toolkit')

# Main function 
# -------------


opening_text = '***************************\n'
opening_text += '* CDG Prepare dataset    *\n'
opening_text += '***************************\n'
opening_text += 'Datasets available: %s.\n' % str(available_datasets.keys())
opening_text += 'Author: Daniele Zambon\n'
opening_text += 'eMail: daniele.zambon@usi.ch\n'
opening_text += 'last update: %s\n\n' % last_update



def main(argv):
    print(opening_text)
    args = parser.parse_args()
    classes = [int(item) for item in args.classes.split(',')]
    gmt = cdg.graph.dissimilarity.GMT(
        executable='./graph-matching-toolkit/graph-matching-toolkit.jar')
    dataset = cdg.graph.database.Script(args.tmp_path, dissimilarity_instance=gmt)

    grah_name_map_file =  os.path.join(args.tmp_path, "graph_name.map")

    if not os.path.exists(grah_name_map_file):
        dataset.generate_new_dataset(data_path=args.data_path, classes=classes, format=['gxl'])

    dataset.load_graph_name_map()

    graph_list = []
    for i in range(len(dataset.get_all_elements())):
        gxl_path = dataset.path + "/" + dataset.get_name_and_class(i)[1]
        print(gxl_path)
        graph = cdg.graph.graph.Graph(filename=gxl_path)
        graph.load()
        nx_graph = nx.drawing.nx_pydot.from_pydot(graph.pydot())
        graph_list.append(nx_graph)
        save_to_png = dataset.path + "/graphs/" + nx_graph.graph['name']
        #plot_graph(nx_graph, save_to_png)
        print("The num of nodes and edges of Graph %s : " % nx_graph.graph['name'], 
                      nx_graph.number_of_nodes(), nx_graph.number_of_edges())


    # each item in graph_list is networkx.classes.multidigraph.MultiDiGraph object
    print(graph_list[0])
    plot_graph(graph_list[0], "dd")


#    pg = PatternGraph.PatternGraph(graph_list[0], graph_list[0].graph['name'])
#    print(pg.get_edges())
#    print(pg.get_nodes())



if __name__ == "__main__":
    main(sys.argv[1:])