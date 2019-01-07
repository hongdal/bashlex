import bashlex

f = "./graphs/testcase/or.sh"
cmd = ""
with open(f) as infile:
    lines = infile.readlines()
    for line in lines:
        cmd += line 

parts = bashlex.parse(cmd)
for ast in parts:
    print(ast.dump())




