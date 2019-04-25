import pprint
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
        print("Usage: " + sys.argv[0] + " <path-to-infile.out> <path-to-capability.json>")
        exit(1)

    infile = sys.argv[1]
    cfile = sys.argv[2]
    graph = BashGraph()
    graph.load_file(infile)
    graph.make_graph()
    cfg = graph.get_graph()

    automaton = Automaton()
    automaton.load_capabilities(cfile)
    automaton.update_with_cfg(cfg)

    automaton.print_automaton()
    automaton.print_edges()
    exit(0)

    json = json.dumps(automaton.automaton)
    printer = pprint.PrettyPrinter(indent=4, width=96, depth=10, compact=True)
    printer.pprint(json)




