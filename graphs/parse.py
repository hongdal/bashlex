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


def read_file(fname):
    regex = r"([a-zA-Z]+)(Node)"
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


class NodeData(object):

    def __init__(self, level, kind, label):
        self.kind = kind
        self.label = label


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
        self.current.add_child(node)
        if ((node.data.kind == "WordNode") or
            (node.data.kind == "PipeNode") or 
            (node.data.kind == "ReservedwordNode") or 
            (node.data.kind == "OperatorNode") or
            (node.data.kind == "RedirectNode")):
            pass
        else: 
            self.push_track_depth.append(node)
        self.current = node

    def push_width(self, node):
        self.current.add_child(node)

    def traverse_depth(self, node):
        






if __name__ == "__main__": 
    pass
