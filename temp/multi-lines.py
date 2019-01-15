import bashlex
import sys 


if len(sys.argv) < 2:
    print("usage: %s <infile.sh>" % sys.argv[0])
    exit(0)

f = sys.argv[1]
cmd = ""
with open(f) as infile:
    lines = infile.readlines()
    for line in lines:
        cmd += line 

parts = bashlex.parse(cmd)
for ast in parts:
    print(ast.dump())




