import pprint
import glob
import json
import sys
import os 
sys.path.append("../bashlex")
import bashlex 
sys.path.append("../bashgraph")
from bashgraph import BashGraph
sys.path.append("../automaton")
from automaton import Automaton


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " <testcase_dir> <path-to-capability.json>")
        exit(1)

    test_dir = sys.argv[1]
    cfile = sys.argv[2]
    in_files = glob.glob(test_dir + "/*.node")
    automaton = Automaton()
    automaton.load_capabilities(cfile)
    for in_file in in_files:
        print("Update with %s ..." % in_file)
        graph = BashGraph()
        graph.load_file(in_file)
        graph.make_graph()
        cfg = graph.get_graph()
        automaton.update_with_cfg(cfg)
    #automaton.print_automaton()
    #automaton.print_edges()
    #encoded_automaton = automaton.dump_automaton()
    #print(encoded_automaton)
    automaton.write_automaton_to_file("./automaton.json")
    orig_automaton = automaton.automaton 
    automaton.read_automaton_from_file("./automaton.json")
    new_automaton = automaton.automaton
    print(orig_automaton == new_automaton)
    exit(0)

    json = json.dumps(automaton.automaton)
    printer = pprint.PrettyPrinter(indent=4, width=96, depth=10, compact=True)
    printer.pprint(json)


