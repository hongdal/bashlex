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
        self.commands = []
        self.connectors = []

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
            if ("WordNode" == child.data.kind or 
                "AssignmentNode" == child.data.kind):
                command.append(child.data.label)
            elif ("RedirectNode" == child.data.kind or 
                "CommandNode" == child.data.kind):
                command = command + self.make_command(child)
            else:
                print("Not a WordNode:%s" % child.data.kind)
                exit(1)
        return command

    '''
        Get a commnad list that lists all commands
    '''
    def get_commands(self, node):
        commands = []
        if ("CommandNode" == node.data.kind or 
            "RedirectNode" == node.data.kind):
            command = self.make_command(node)
            return [command]
        else:
            for child in node.children:
                commands = commands + self.get_commands(child)
        return commands


    '''
        Get a command chain. This function fills two lists

        commands = [[w1, w2,...], [w1, w2, ...], ...]
        connectors = [[[con1], [con2],...], [[conn3],[conn3],...]]

        Use preorder to first collect the connetor (internal nodes),
        then collect the commands (leaf nodes)

    '''
    def recursive_update_command_connectors(self, node):
        # If this is a command node        
        if ("CommandNode" == node.data.kind or
            "RedirectNode" == node.data.kind):
            command = self.make_command(node)
            # cat each words in a command
            cat_command = "" 
            for word in command:
                cat_command += word + " "
            # add this command to the commands list. 
            self.commands.append([cat_command])
            # add a new bucket for the connector connecting to next command
            self.connectors.append([])

        # If they are connector nodes
        elif ("PipNode" == node.data.kind):
            # push to the latest connector collection
            (self.connectors[-1]).append(["|"])
        elif ("OperatorNode" == node.data.kind):
            (self.connectors[-1]).append([node.data.label])
        elif ("CompoundNode" == node.data.kind):
            (self.connectors[-1]).append(["SC"])
        elif ("ReservedwordNode" == node.data.kind):
            (self.connectors[-1]).append([node.data.label])
        elif ("ListNode" == node.data.kind):
            pass
        elif ("WordNode" == node.data.kind):
            pass
        elif ("Root" == node.data.kind):
            pass
        else:
            #print(node.data.kind)
            (self.connectors[-1]).append(["N"])

        # Traverse the tree
        for child in node.children:
            self.recursive_update_command_connectors(child)


    def update_command_connectors(self):
        self.commands = []
        self.connectors = [[]]
        self.recursive_update_command_connectors(self.root)


    '''
        print all commands
    '''
    def dump_commands(self, root):
        commands = self.get_commands(root)
        for command in commands:
            if None != command:
                ret = ""
                for word in command:
                    ret = ret + word + " "
                print(ret)

    '''
        print commands and connectors
        return value:
        [[last_cmd, current_cmd, connector],[last_cmd, current_cmd, connector],...]
    '''
    def dump_command_connectors(self):
        ret = []
        length = len(self.commands)
        if  0 == length:
            pass
        elif 1 == length:
            ret.append([self.commands[0], "", ""])
        else:
            index = 1
            last_command = self.commands[0]
            while (index < length):
                command = self.commands[index]
                connector = self.connectors[index-1]
                output = last_command[0] + "-->" + command[0] + "==>"
                connectors = ""
                for c in connector:
                    if (c[0] == "\n"):
                        connectors += r"\n" + r","
                    else:
                        connectors = connectors + c[0] + r","
                output = output + connectors + "\n"
                # print(output)
                # dump to a list
                ret.append([last_command[0], command[0], connectors])
                # update iteration
                index += 1
                last_command = command
        return ret 

    def dump_leaves(self, node):
        if len(node.children) == 0:
            print(node.data.label, end=" ")
        else:
            for child in node.children:
                self.dump_leaves(child)


"""
Begin of procedures. 

"""


'''
    Use command as an index indead of as a value. 
    So, same command is mapped to the same id. 

    If you want to print the same command as multiple nodes, 
    use id as index and command as value. 
'''
def print_graph(node_list):
    # delete double qoutes
    for element in node_list:
        element[0] = element[0].replace(r'"', r'\"')
        element[1] = element[1].replace(r'"', r'\"')
        element[2] = element[2].replace(r'"', r'\"')
    # give ids
    graph = {}
    id = 0
    for element in node_list:
        if "" != element[0]:
            graph[element[0]] = id
            id += 1
            if "" != element[1]:
                graph[element[1]] = id 
                id += 1
    # print graph
    print("digraph {")
    for element in node_list:
        line = ""
        if "" != element[0]:
            # print label
            print('%s [label="%s"];' % (str(graph[element[0]]), element[0]) )
            # print connection
            line += str(graph[element[0]]) + " -> "
            if ("" != element[1] and "" != element[2]):
                line += str(graph[element[1]]) 
                line += ' [label="' + element[2] + '"];'
            else:
                line += str(graph[element[0]])
            print(line)

    print("}")

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
    with open("./testcase/3.out") as fp:
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
    #tree.dump_leaves(tree.root)
    #tree.dump_commands(tree.root)
    tree.update_command_connectors()
    node_list = tree.dump_command_connectors()
    print_graph(node_list)
    #print(tree.commands)