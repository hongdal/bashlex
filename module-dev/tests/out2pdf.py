import glob
import sys
import os 
sys.path.append("../bashgraph")
from bashgraph import BashGraph 
import subprocess

def out2pdf(in_file, out_dir):
    basename = os.path.basename(in_file)[:-4]
    out_dir = out_dir + "/"
    tmp_dir = out_dir + "tmp/"
    tmp_file = tmp_dir + basename + ".dot"
    out_file = out_dir + basename + ".pdf"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    orig_stdout = sys.stdout
    g = BashGraph()
    g.load_file(in_file)
    g.make_graph()
    sys.stdout = open(tmp_file, "w")
    g.print_graph()
    sys.stdout = orig_stdout 
    command = ['dot', '-Tpdf', tmp_file, '-o', out_file]
    subprocess.check_call(command)
    command = ['rm', '-rf', tmp_dir]
    subprocess.check_call(command)
    return out_file


ret = out2pdf(sys.argv[1], sys.argv[2])
print(ret)
