import glob
import sys
import os 
sys.path.append("../bashlex")
import bashlex
sys.path.append("../bashgraph")
from bashgraph import BashGraph


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <testcase_dir>")
        exit(1)

    test_dir = sys.argv[1]
    
    # 
    # Generate .out files. 
    # Comment out if you don't want. 
    #
    bash_files = glob.glob(test_dir + "/*.sh")
    orig_std = sys.stdout
    for bash_file in bash_files:
        print("Parsing %s ..." % bash_file)
        basename = os.path.splitext(bash_file)[0]
        cmd = ""
        with open(bash_file) as infile:
            lines = infile.readlines()
            for line in lines:
                cmd += line 
        parts = bashlex.parse(cmd)
        sys.stdout = open(basename + ".out", "w")
        for ast in parts:
            print(ast.dump())
        sys.stdout = orig_std

    # 
    # Compute graph 
    # 
    out_files = glob.glob(test_dir + "/*.out")
    orig_std = sys.stdout 
    for out_file in out_files:
        print("Printing %s ..." % out_file)
        basename = os.path.splitext(out_file)[0]
        graph = BashGraph()
        graph.load_file(out_file)
        graph.make_graph()
        sys.stdout = open(basename + ".dot", "w")
        graph.print_graph()
        sys.stdout = orig_std


