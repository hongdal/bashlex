from ast import NodeData, Node, Tree
from visitor import TreeVisitor
import re 

regex = r"([a-zA-Z]+)(Node)"

def parse_WordNode(line):
    target = r", word=([^,;\n])+"
    match = re.search(target, line)
    if None == match:
        label = ""
    else:
        label = re.sub(r"^(, word=')", '', match.group(0))
        label = re.sub(r"(')$", '', label)
        label = re.sub(r"('\))$", '', label)
    return label

def parse_OperatorNode(line):
    target = r", op='([\\;\&\|])*(n)*"
    match = re.search(target, line)
    if None == match:
        label = ""
    else:
        label = re.sub(r"^(, op=')", '', match.group(0))
    if r"\n" == label:
        label = "\n"    
    return label


def parse_ReservedwordNode(line):
    target = r", word=([^,;\n])+"
    match = re.search(target, line)
    if None == match:
        label = ""
    else:
        label = re.sub(r"^(, word=')", '', match.group(0))
        label = re.sub(r"(')$", '', label)
        label = re.sub(r"('\))$", '', label)
    # make it a little bit good looking. 
    #if ("then" == label or "do" == label or "fi" == label or 
    #    "done" == label or "else" == label):
    #    label = label + "\n"
    return label


def parse_AssignmentNode(line):
    target = r", word=([^,;\n])+"
    match = re.search(target, line)
    if None == match:
        label = ""
    else:
        label = re.sub(r"^(, word=')", '', match.group(0))
        label = re.sub(r"(')$", '', label)
        label = re.sub(r"('\))$", '', label)
    return label


def parse_ParameterNode(line):
    target = r", value=([^,;\n])+"
    match = re.search(target, line)
    if None == match:
        label = ""
    else:
        label = re.sub(r"^(, value=')", '', match.group(0))
        label = re.sub(r"(')$", '', label)
        label = re.sub(r"('\))$", '', label)
    return label


def parse_node(line, kind, indent):
    # assign label to each node. 
    if "WordNode" == kind:
        label = parse_WordNode(line)
    elif "OperatorNode" == kind:
        label = parse_OperatorNode(line)
    elif "ReservedwordNode" == kind:
        label = parse_ReservedwordNode(line)
    elif "AssignmentNode" == kind:
        label = parse_AssignmentNode(line)
    elif "ParameterNode" == kind:
        label = parse_ParameterNode(line)
    else:
        label = ""
    data = NodeData(int(indent)/2, kind, label)
    node = Node(data, 0)
    return node


def read_file(fname):
    with open(fname) as fp:
        line = fp.readline()
        while line:
            # count leading space
            lspace = len(line) - len(line.lstrip())
            # search for the node type
            node = re.search(regex, line)
            if None == node:
                pass
            else:
                print("%d,%s" % (lspace, node.group(0)))
            line = fp.readline()


class BashGraph:

    def __init__(self):
        self.fname = ""
        self.tree = None
        self.visitor = None

    def load_file(self, fname):
        self.fname = fname
        self. tree = Tree(Node(NodeData(-1, "Root", "Start"), 0))
        with open(self.fname) as fp:
            line = fp.readline()
            while line:
                # Count leading space
                lspace = len(line) - len(line.lstrip())
                # Search for the node type. 
                node = re.search(regex, line)
                # we found a match
                if None != node:
                    new_node = parse_node(line, node.group(0), lspace)
                    if None != new_node:
                        self.tree.push_depth(new_node)
                line = fp.readline() 


    def make_graph(self):
        if None == self.tree:
            print(".out file is not loaded, use load_file() first.")
            return
        self.visitor = TreeVisitor(self.tree)
        self.visitor.make_cfg()
        self.visitor.build_cfg()


    def print_graph(self):
        if None == self.visitor:
            print("AST is not retrieved, use make_graph() first.")
            return
        self.visitor.print_cfg()


    def get_graph(self):
        if None == self.visitor:
            print("AST is not retrieved, use make_graph() first.")
            return
        return self.visitor.cfg

