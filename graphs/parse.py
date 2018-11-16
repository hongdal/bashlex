#!/usr/bin/env python
# coding=utf-8

import os
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
        self.push_track_depth = [self.root]

    def push_depth(self, node):
        # change current pointers
        last = self.current
        '''
        print("current:%d" % (node.data.level), end=",")
        print("last:%d" % last.data.level, end="->")
        print("[", end="")
        for i in self.push_track_depth:
            print(",%d" % i.data.level, end="")
        print("]", end="->")
        print("length:%d" % len(self.push_track_depth))
        '''

        # If last node.level >= new node.level, pop out
        while not (last.data.level < node.data.level): 
            self.push_track_depth.pop()
            last = self.push_track_depth[-1]
        # do insert
        last.add_child(node)
        self.current = node
        self.push_track_depth.append(node)
        #
        # if ((node.data.kind == "WordNode") or
        #     (node.data.kind == "PipeNode") or 
        #     (node.data.kind == "ReservedwordNode") or 
        #     (node.data.kind == "OperatorNode") or
        #     (node.data.kind == "RedirectNode")):
        #     pass
        # else: 
        #     self.push_track_depth.append(node)

    def push_width(self, node):
        pass 


    '''
        I assume commands are consist of words. 

        It's important to notice that a WordNode is possible 
        to be an internal node. In this case, the word is expand
        through a CommnadSubstitutionNode. 

        I would like to create a separate graph for all the substitution nodes. 

        Another issue is that a command may consist of other kinds of nodes,
        e.g., redirectNode (see test-parser.py) 
        I have not considered that yet. 

        Now I assume redirect commnads are consist of words

    '''
    def make_command(self, node):
        command = []
        for child in node.children:
            if ("WordNode" == child.data.kind):
                command.append(child.data.label)
            else:
                print("Not a WordNode")
                exit(1)
        return command

    def get_commands(self, node):
        commands = []
        if ("CommandNode" == node.data.kind or 
            "RedirectNode" == node.data.kind):
            command = self.make_command(node)
            return [commnad]
        else:
            for child in node.children:
                commands = commands + self.get_commands(child)
        return commands


    def dump_leaves(self, node):
        if len(node.children) == 0:
            print(node.data.label, end=" ")
        else:
            for child in node.children:
                self.dump_leaves(child)

    def dump_commnads

"""
Begin of procedures. 

"""



def parse_none(line, indent):
    pass


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
    target = r", op='([\\;\&\|])(n)*"
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
    if ("then" == label or "do" == label or "fi" == label or 
        "done" == label or "else" == label):
        label = label + "\n"

    return label


def parse_node(line, kind, indent):
    # assign label to each node. 
    if "WordNode" == kind:
        label = parse_WordNode(line)
    elif "OperatorNode" == kind:
        label = parse_OperatorNode(line)
    elif "ReservedwordNode" == kind:
        label = parse_ReservedwordNode(line)
    elif "ParameterNode" == kind:
        return None
    else:
        label = ""

    data = NodeData(int(indent)/2, kind, label)
    node = Node(data)
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


if __name__ == "__main__": 
    tree = Tree(Node(NodeData(-1, "Root", "Start")))
    with open("./testcase/2.out") as fp:
        line = fp.readline()
        count = 1
        while line:
            # Count leading space
            lspace = len(line) - len(line.lstrip())
            # Search for the node type. 
            node = re.search(regex, line)
            # we found a match
            if None != node:
                new_node = parse_node(line, node.group(0), lspace)
                if None != new_node:
                    tree.push_depth(new_node)
                    #print("%d, %s" % (lspace, node.group(0)))
                    #print(line)
            line = fp.readline()
    tree.dump_leaves(tree.root)