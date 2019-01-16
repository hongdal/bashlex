#!/usr/bin/env python
# coding=utf-8

import os
import re
import sys

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
    "RedirectNode",
    "WhileNode",
    "ParameterNode",
    "PipeNode",
    "AssignmentNode",
    "ForNode"
]

regex = r"([a-zA-Z]+)(Node)"

class NodeData(object):
    
    '''
        kind        :   which kind of node, node name. 
        label       :   the string label of the node. 
        level       :   at which nested level. 
        tails       :   a set of the last commands of this node if its a compound 
                        node (e.g., IfNode, WhileNode). If it's a CommandNode, 
                        this points to itself. When you add a new tail to this node, 
                        if it's from another compound node, then a list of CommandNode
                        will be merged (remove duplications) to this list. 
                        A special case is '&&' and '||'.
                        Commands on the left and right of '&&' ('||')
                        should be included in the tails. 

        precursors  :   a set of precursors of this node. When you add a new 
                        precursors to this node, if it's a compound node, then 
                        a list of CommandNode will be merged (remove duplications)
                        to this list. 
                        A special case is '&&' and '||'.
                        Commands on the left and right of '&&' ('||')
                        should be included in the precursor.

        continues   :   a set of the "continue" commands inside a For node or While node.
                        If a node is a ForNode or WhileNode, it will not report to its 
                        parent any information about continue. 
                        If a node is a normal command node, it will ask its children and 
                        report to its parent any information about continue. 
                        If a node is a basic command node, it will be checked whether it's
                        a "continue" command. 


        Let me explain how to add tails and precursors. 
        1) tails. 
            If it's a CommandNode, the tails only contains itself. 
            If it's an IfNode, then tails contains the tails of the last command in each condition and body lists. 
            If it's a WhileNode, the tails contains the tails of the last command in condition and body lists. 
            If it's a ForNode, the tails contains the tails of the last command in the body. 
            The last command of a list is defined as follows. 
            (1) last command of If condition is followed by a ReservedwordNode('then')
            (2) last command of If body is followed by a ReservedwordNode('elif'), 'else', or 'fi'.
            (3) last command of while condition is followed by a ReservedwordNode('do) 
            (4) last command of while body is followed by a ReservedwordNode('done')
            (5) last command of for body is followed by a ReservedwordNode('done')
            (6) If a command is followed by '&&' or '||', then  it must be considered 
            simultaneously as the one after the '&&' ('||') operator.

            The challenge is how to identify 'last command'. 

        2) precursors.
            This points to the tails of the command immediately before the current
            command. 

            The challenge is how to define a command. 

            A commnad must be represented by one of the following nodes. 
            list-1:
            (1) ListNode
            (2) CompoundNode
            (3) IfNode
            (4) WhileNode
            (5) ForNode
            (6) CommandNode
            (7) CommandsubstitutionNode
            (8) PipelineNode
            (9) WordNode - because of substitution
            (10) AssignmentNode - because of substitution

            The following should not be a command. 
            list-2:
            (1) ReservedwordNode
            (2) ParameterNode
            (3) OperatorNode
            (4) RedirectNode
            (5) PipeNode

            If a node meets the following condition, it represents 
            a basic command. 
            (1) Only WordNode and nodes in list-2 are included in the paths 
            from it to the leaves. 


    '''

    def __init__(self, level, kind, label):
        self.kind = kind
        self.label = label
        self.level = level
        self.tails = set([])
        self.precursors = set([])
        self.continues = set([])
        self.pre = None


class Node(object):

    def __init__(self, data, uid):
        self.data = data
        self.children = []
        self.parent = None
        self.uid = uid    # for graph to uniquly identify a node. 

    def add_child(self, obj):
        self.children.append(obj)

    def set_parent(self, obj):
        self.parent = obj

'''
root                : the root of the tree. 
current             : the node that is at the end of the stack. 
push_track_depth    : a stack containing the path from @current to @root. 
commands            : 

'''
class Tree(object):
    
    def __init__(self, node):
        self.root = node
        self.current = self.root
        self.push_track_depth = [self.root]
        self.commands = []
        self.connectors = []
        # uniquely identify a node in the tree
        self.accumulate_uid = 0

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

        # The key idea is to find the parent of @node. 
        # Pop the stack until @last has smaller level than @node. 
        # In this case, @node is going to be the child of @last.  
        while not (last.data.level < node.data.level): 
            self.push_track_depth.pop()
            last = self.push_track_depth[-1]
        # do insert
        last.add_child(node)
        node.set_parent(last)
        self.accumulate_uid += 1
        node.uid = self.accumulate_uid
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


class TreeVisitor:
    def __init__(self, tree):
        self.tree = tree
        self.current_path_to_root = []
        self.level = -1
        self.basic_commands = []
        self.cfg = {}


    def make_cfg(self):
        self.recursive_visit(self.tree.root)


    '''
        Check whether WordNode and AssignmentNode is expandable or not. 
    ''' 
    def is_expandable(self, node):
        for c in node.children:
            if c.data.kind == "CommandsubstitutionNode":
                return True 
        return False

    '''
        node    : the "Root" node
    '''
    def visit_root_node(self, node):
        is_first_command = True 
        last_command_child = None 
        node.data.precursors = set([])
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may skip
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    # skip if it's not expandable. 
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)
        if last_command_child == None:
            print("Node:%s does not have command children\n" % node.data.kind)
            exit(1)


    def visit_command_node(self, node):
        is_first_command = True
        last_command_child = None
        # If it's a basic command 
        if self.is_basic_command(node):
            # check whether it's "continue"
            if -1 != node.children[0].data.label.find("continue"):
                # 4) compute the continues of the node itself
                node.data.continues.add(node)
                # 5) compute the tails of the node itself, set it to empty.
                node.data.tails = set([])
                return
        # Otherwise it's not a basic command, let's expand it. 
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 5) compute the continues of the node itself
                # It's impossible for a CommandNode has a child that contains "continue"
                # node.data.continues = node.data.continues.union(last_command_child.data.continues)

        # 4) compute the tails of the node itself 
        if last_command_child == None:
            # If all its children are not expandable then use its own as its tail. 
            node.data.tails.add(node)
        else:
            node.data.tails = last_command_child.data.tails

    def visit_list_compound_node(self, node):
        is_first_command = True
        last_command_child = None
        # To handle "||" and "&&" operators
        local_tails = []
        local_tails_terminating = False
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # Handle "||" and "&&" operators
                if node.children[i].data.kind == "OperatorNode":
                    if None == last_command_child:
                        print("Syntax issue: %s operator at the beginning." % node.children[i].data.label)
                        exit(1)
                    if node.children[i].data.label == r"||" or \
                       node.children[i].data.label == r"&&":
                        local_tails.append(last_command_child.data.tails)
                        local_tails_terminating = False
                    else:
                        local_tails_terminating = True
                    continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    # Handle "||" and "&&" operators
                    if True == local_tails_terminating and len(local_tails) > 0:
                        for local_tail in local_tails:
                            node.children[i].data.precursors = node.children[i].data.precursors.union(local_tail)
                        local_tails_terminating = False
                        local_tails = []

                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)
        if last_command_child == None:
            print("Node:%s does not have command children\n" % node.kind)
            exit(1)
        

    def visit_word_assignment_node(self, node):
        is_first_command = True
        last_command_child = None
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            # Only when it's substitution, expand it. 
            if node.children[i].data.kind == "CommandsubstitutionNode":
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)

    '''
        if condition; then 
            command
        elif condition; then
            command
        else
            command
        fi
    '''
    def visit_if_node(self, node):
        # Seperate conditions and bodies
        conditions = []
        bodies = [] 
        for i in range(len(node.children)):
            if node.children[i].data.kind == "ReservedwordNode":
                if (node.children[i].data.label == "if" or node.children[i].data.label == "elif"):
                    conditions.append(node.children[i+1])
                if (node.children[i].data.label == "then" or node.children[i].data.label == "else"):
                    bodies.append(node.children[i+1])
        if len(conditions) != len(bodies)-1 and len(conditions) != len(bodies):
            print("If-else condition and body mismatch\n")
            exit(1)

        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(conditions)):
            # 1) compute the precursors of all the conditions
            if 0 == i:
                conditions[i].data.precursors = node.data.precursors
            else:
                conditions[i].data.precursors = conditions[i-1].data.tails
            # 2) compute tails of all conditions
            # 3) compute the continues of all conditions
            self.recursive_visit(conditions[i])

        for i in range(len(conditions)):
            # 1) compute the precursors of all bodies
            bodies[i].data.precursors = conditions[i].data.tails 
            # 2) compute tails of all bodies
            # 3) compute the continues of all bodies
            self.recursive_visit(bodies[i])
            # 5) compute the continues of the node itself
            node.data.continues = node.data.continues.union(bodies[i].data.continues)

        # One more body, caused by "else"
        if len(bodies) > len(conditions):
            # 1) compute the precursors of last body 
            bodies[-1].data.precursors = conditions[-1].data.tails
            # 2) compute tails of all last body
            # 3) compute the continues of last body
            self.recursive_visit(bodies[-1])
            # 5) compute the continues of the node itself
            node.data.continues = node.data.continues.union(bodies[-1].data.continues)

        # 4) compute the tails of the IfNode, 
        # using all bodies and the last condition. 
        for i in range(len(bodies)):
            node.data.tails = node.data.tails.union(bodies[i].data.tails)
        node.data.tails = node.data.tails.union(conditions[-1].data.tails)


    def visit_commandsubstitution_node(self, node):
        is_first_command = True
        last_command_child = None
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)
                    
        if last_command_child == None:
            print("Node:%s does not have command children\n" % kind)
            exit(1)

    def visit_pipeline_node(self, node):
        is_first_command = True
        last_command_child = None
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)

        if last_command_child == None:
            print("Node:%s does not have command children\n" % node.kind)
            exit(1)

    '''
        For word in word; do 
            command
        done
    '''
    def visit_for_node(self, node):
        is_first_command = True
        last_command_child = None
        first_body = None
        continues_from_children = set([])
        node.data.continues = set([])
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 5) compute the continues of the node itself
                continues_from_children = continues_from_children.union(last_command_child.data.continues)
            # set the first command of the body
            if node.children[i].data.kind == "ReservedwordNode" and \
                node.children[i].data.label == "do":
                first_body = node.children[i+1]

        # update precursors for the first command of the body, 
        # 1) adding tails of the body as the precursors of the first command of the body 
        # 2) adding continues of its children as the precursors of the first command of the body
        # And update all its children
        first_body.data.precursors = first_body.data.precursors.union(last_command_child.data.tails)
        first_body.data.precursors = first_body.data.precursors.union(continues_from_children)
        self.recursive_visit(first_body)

        # 4) compute the tails of the node itself 
        if last_command_child == None:
            print("Node:%s does not have command children\n" % node.kind)
            exit(1)
        else:
            node.data.tails = last_command_child.data.tails.union(continues_from_children)


    '''
        while command; do 
            command 
        done
    '''
    def visit_while_node(self, node):
        # Match the while node pattern
        # while + condition + do + body + done
        if len(node.children) != 5:
            print("Bad WhileNode: lenght=%d\n" % len(node.children))
            exit(1)
        elif node.children[0].data.kind != "ReservedwordNode" or \
                node.children[2].data.kind != "ReservedwordNode":
            print("Bad WhileNode: lenght=%d\n" % len(node.children))
            exit(1)
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        # match the while node condition and body. 
        condition_command_child = node.children[1]
        body_command_child = node.children[3]
        # 1) compute the precursors of the condition
        condition_command_child.data.precursors = node.data.precursors 
        # 2) compute tails of all the condition
        self.recursive_visit(condition_command_child)
        # 1) compute the precursors of the body
        body_command_child.data.precursors = condition_command_child.data.tails
        # 2) compute tails of all the body
        self.recursive_visit(body_command_child)
        # update precursors for condition, 
        # 1) adding tails of body to the condition
        # 2) adding continues in the body to the condition
        condition_command_child.data.precursors = condition_command_child.data.precursors.union(body_command_child.data.tails)
        condition_command_child.data.precursors = condition_command_child.data.precursors.union(body_command_child.data.continues)
        # update all children of condition nodes. 
        # Update precursors of all the children in the condition. 
        self.recursive_visit(condition_command_child)

        # 4) compute the tails of the node itself 
        node.data.tails = condition_command_child.data.tails
        # 5) compute the continues of the node itself
        node.data.continues = set([])

    """
        Set tails of node and 
        Set precursors and tails of its children
    """
    def recursive_visit(self, node):
        kind = node.data.kind
        if "ReservedwordNode" == kind or "ParameterNode" == kind or \
            "OperatorNode" == kind or "RedirectNode" == kind or \
            "PipeNode" == kind:
            node.data.tails = None
            return
        if "Root" == kind:
            self.visit_root_node(node)
        #
        #   Todo: handle "||" and "&&" operation
        #
        elif "ListNode" == kind or "CompoundNode" == kind:
            self.visit_list_compound_node(node)
        elif "WordNode" == kind or "AssignmentNode" == kind:
            self.visit_word_assignment_node(node)
        elif "IfNode" == kind:
            self.visit_if_node(node)
        elif "WhileNode" == kind:
            self.visit_while_node(node)
        elif "ForNode" == kind:
            self.visit_for_node(node)
        elif "CommandNode" == kind:
            self.visit_command_node(node)
        elif "CommandsubstitutionNode" == kind:
            self.visit_commandsubstitution_node(node)
        elif "PipelineNode" == kind:
            self.visit_pipeline_node(node)
        else:
            print("Unknown kind:%s" % kind)
            exit(2)


    def dump_tree(self):
        self.level = -1
        self.recursive_dump_node(self.tree.root)

    def recursive_dump_node(self, node):
        self.level +=  1
        # dump itself. 
        #indent = "  " * int(node.data.level+1)
        indent = "  " * int(self.level)
        content = node.data.kind + "(" + node.data.label + ")"
        print(indent + content)
        for child in node.children:
            self.recursive_dump_node(child)
        self.level -= 1



    def is_basic_command(self, node):
        for child in node.children:
            if "WordNode" == child.data.kind or "AssignmentNode" == child.data.kind:
                if self.is_expandable(child):
                    return False
            elif "ListNode" == child.data.kind or "CompoundNode" == child.data.kind or \
                "IfNode" == child.data.kind or "WhileNode" == child.data.kind or \
                "ForNode" == child.data.kind or "CommandNode" == child.data.kind or \
                "CommandsubstitutionNode" == child.data.kind or "PipelineNode" == child.data.kind:
                return False
            else:
                continue
        return True


    '''
        node must be a basic command, i.e., not expandable any more
    '''
    def label_basic_command(self, node):
        command = ''
        for child in node.children:
            command += " " + child.data.label
        command = command.replace(r'"', r'\"')
        command = command.replace(r'[', r'\[')
        command = command.replace(r']', r'\]')
        node.data.label = command


    def build_basic_commands(self, node):
        # determine whether it's a basic command. 
        if node.data.kind == "CommandNode":
            # Add a new record to the hash table if it's a basic command. 
            if self.is_basic_command(node):
                self.basic_commands.append(node)
                # update the label of node - This must be the basic command
                self.label_basic_command(node)
                return
        for child in node.children:
            self.build_basic_commands(child)
                

    def build_cfg(self):
        self.basic_commands = []
        self.build_basic_commands(self.tree.root)
        self.cfg = {}
        # traverse the basic command list
        for basic_command in self.basic_commands:
            for precursor in basic_command.data.precursors:
                if precursor in self.cfg:
                    self.cfg[precursor].append(basic_command)
                else:
                    self.cfg[precursor] = [basic_command]


    def print_cfg(self):
        print("digraph {")
        # Print all the nodes that are followed by other nodes. 
        for key in self.cfg.keys():
            labeling_node = str(key.uid) + ' [label="' + key.data.label + '"];'
            print(labeling_node)
            for node in self.cfg[key]:
                connection = str(key.uid) + ' -> ' + str(node.uid) + ';'
                print(connection)
        print("}")




'''
    The key idea is to parse the .out file line by line. 
    Then we get a hierarchical structure like this: 

    IfNode(
        ReservedwordNode('if')
        ListNode(
            CommandNode('[...]')
            OperatorNode(';')
        )
        ReservedwordNode('then')
        ListNode(
            CommandNode('...')
            OperatorNode(';)
            CommandNode('...')
            OperatorNode('\n')
        )
        ReservedwordNode('elif')
        ListNode(
            CommandNode('...')
            OperatorNode('\n')
            CommandNode('...')
            OperatorNode('\n')
        )
        ReservedwordNode('then)
        ListNode(
            CommandNode('...')
            OperatorNode('\n')
            CommandNode('...')
            OperatorNode('\n')
        )
        ReservedwordNode('else')
        ListNode(
            CommandNode('...')
            OperatorNode('\n')
            CommandNode('...')
            OpeartorNode(';')
        )
        ReservedwordNode('fi')
    )

    To be simple, lets denote it as follows. 

    IfNode
        ReservedwordNode(if)
        ListNode(condition1)
            CommandNode(1)
            CommandNode(2)
        ReservedwordNode(then)
        ListNode(body1)
            CommandNode(3)
            CommandNode(4)
        ReservedwordNode(elif)
        ListNode(condition2)
            CommandNode(5)
            CommandNode(6)
        ReservedwordNode(then)
        ListNode(body2)
            CommandNode(7)
            CommandNode(8)
        ReservedwordNode(else)
        ListNode(body3)
            CommandNode(9)
            CommandNode(10)
        ReservedwordNode(fi)


    Then let's consider IfNode as a blackbox, we get this.


    ListNode
        CommandNode(s)
        CompoundNode
            IfNode
        CommandNode(s)


    We want to make the follwoing connections 
        CommandNode(s) -> CommandNode(1)
        CommandNode(1) -> CommandNode(2)
        CommandNode(2) -> CommandNode(3)
        CommandNode(2) -> CommandNode(5)
        CommandNode(2) -> CommandNode(9)
        CommandNode(2) -> CommandNode(e)
        CommandNode(3) -> CommandNode(4)
        CommandNode(4) -> CommandNode(e)
        CommandNode(5) -> CommandNode(6)
        CommandNode(6) -> CommandNode(7)
        CommandNode(6) -> CommandNode(9)
        CommandNode(6) -> CommandNode(e)
        CommandNode(7) -> CommandNode(8)
        CommandNode(8) -> CommandNode(4)
        CommandNode(9) -> CommandNode(10)
        CommandNode(10) -> CommandNode(e)

    Lets group the connections as follows. 

    (1): What is the first command in IfNode?
        CommandNode(s) -> CommandNode(1)

    (2): What are the connections within an IfNode?
        CommandNode(2) -> CommandNode(3)
        CommandNode(2) -> CommandNode(5)
        CommandNode(2) -> CommandNode(9)
        CommandNode(6) -> CommandNode(7)
        CommandNode(6) -> CommandNode(9) 
        ... 

    (3): How do the command get merged?
        CommandNode(2) -> CommandNode(e)
        CommandNode(4) -> CommandNode(e)
        CommandNode(6) -> CommandNode(e)
        CommandNode(10) -> CommandNode(e)

    Next, let's discuss them one by one. 

    (1): The command immediate after ReservedwordNode('if') is the 
    first command of IfNode. 

    (2): For commands within the same IfNode, the rules are as follows.
    
    1) If a node is in the condition, then its precursors must be the following. 
        + Condition lists before this condition. 

    2) If a node is in the body, then its precursors must be one of the following. 
        + Last commandNode in this body
        + Condition lists before this body

    (3): The last command (let's think nested IfNode as a single command
    within another IfNode) of an IfNode is the union of the last commands
    in each branch body. 
    Then how can we define 'the last command of a branch body'? 
    It is defined as the command immediately before the keywords
    'else', 'elif', and 'fi'.
    If this command is an IfNode, then recursively define it. 
    If this command is a while-do command, it's the union of last command 
    of while condition and its body. 

'''



if __name__ == "__main__": 

    if len(sys.argv) < 2:
        print("Usage: %s <infile.out>" % sys.argv[0])
        exit(0)

    infile = sys.argv[1]
    tree = Tree(Node(NodeData(-1, "Root", "Start"), 0))
    with open(infile) as fp:
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
            line = fp.readline()
    #tree.dump_leaves(tree.root)
    #tree.dump_commands(tree.root)
    
    #tree.update_command_connectors()
    #node_list = tree.dump_command_connectors()
    #print_graph(node_list)
    
    #print(tree.commands) 

    v = TreeVisitor(tree)
    # v.dump_tree()
    v.make_cfg()
    v.build_cfg()
    v.print_cfg()

    