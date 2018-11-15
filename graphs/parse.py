#!/usr/bin/env python
# coding=utf-8

import re

NODE_LIST = [
    "ListNode",
    "CommandNode",
    "OperatorNode",
    "WordNode",
    "CompoundNode",
    "IfNode",
    "ReservedwordNode",
    "CommandsubstitutionNode",
    "PipelineNode",
    "OperatorNode",
    "RedirectNode",
    "WhileNode",
    "RedirectNode",
    "ParameterNode"
]

regex = r"([a-zA-Z]+)(Node)"

class NodeData(object):

    def __init__(self, level, kind, label):
        self.kind = kind
        self.label = label
        self.level = level


class Node(object):

    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


class Tree(object):
    
    def __init__(self, node):
        self.root = node
        self.current = self.root
        self.push_track_depth = []

    def push_depth(self, node):
        # change current pointers
        last = self.current.level
        # If last node.level >= new node.level, pop out
        while not (last.level < node.level): 
            last = self.push_track_depth.pop()
        # now the current points to "last"
        current  = last
        # do insert
        self.current.add_child(node)
        #
        # if ((node.data.kind == "WordNode") or
        #     (node.data.kind == "PipeNode") or 
        #     (node.data.kind == "ReservedwordNode") or 
        #     (node.data.kind == "OperatorNode") or
        #     (node.data.kind == "RedirectNode")):
        #     pass
        # else: 
        #     self.push_track_depth.append(node)
        
        self.current = node

    def push_width(self, node):
        self.current.add_child(node)

    def traverse_depth(self, node):
        pass


"""
Begin of procedures. 

"""
def parse_none(line, indent):
    pass


def parse_node(line, kind, indent):
    data = NodeData(int(indent)/2, kind, kind)
    return Node(data)



def read_file(fname):
    with open(fname) as fp:
        line = fp.readline()
        count = 1
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


if __name__ == "__main__": 
    with open("./testcase/2.out") as fp:
        line = fp.readline()
        count = 1
        while line:
            # Count leading space
            lspace = len(line) - len(line.lstrip())
            # Search for the node type. 
            node = re.search(regex, line)
            if None != node:
                #print("%d, %s" % (lspace, node.group(0)))
                #print(line)
            line = fp.readline()
