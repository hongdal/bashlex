# This script computes the paths. 
# Input:    a folder containing .dot files; a file that will be written to. 
# Output:   a .path file containing all *unique* paths.


import glob 
import sys 
import os 
import re 
sys.path.append("../behavior")
from netnode import netnodex
string = r'[^"]+'

unique_paths = set()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " <.dot foler> <outfile>")
        exit(1)

    test_dir = sys.argv[1]
    outfile = sys.argv[2]
    dot_files = glob.glob(test_dir + "/*.dot")
    orig_std = sys.stdout
    for dot_file in dot_files:
        print("Extracting %s ..." % dot_file)
        nd = netnodex()
        nd.read_from_dot(dot_file)
        nd.load_node_names()
        all_paths = nd.get_start_to_end_paths()
        nd.condense_all_paths()
        sp = nd.get_path_with_length(0, 1000)
        unique_paths.update(sp)
    
    with open(outfile, "w") as new_stdout:
        sys.stdout = new_stdout
        for path in unique_paths:
            for cmd in path:
                m = re.search(string, cmd)
                if None != m:
                    sys.stdout.write(m.group(0) + ",")
            sys.stdout.write("\n")



