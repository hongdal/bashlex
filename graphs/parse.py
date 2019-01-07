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
        tails       :   a list of the last commands of this node if its a compound 
                        node (e.g., IfNode, WhileNode). If it's a CommandNode, 
                        this points to itself. When you add a new tail to this node, 
                        if it's from another compound node, then a list of CommandNode
                        will be merged (remove duplications) to this list. 
                        A special case is '&&' and '||'.
                        Commands on the left and right of '&&' ('||')
                        should be included in the tails. 

        precursors  :   a list of precursors of this node. When you add a new 
                        precurosr to this node, if it's a compound node, then 
                        a list of CommandNode will be merged (remove duplications)
                        to this list. 
                        A special case is '&&' and '||'.
                        Commands on the left and right of '&&' ('||')
                        should be included in the precurosrs.

        simult      :   used to collect the CommandNode right before '&&' and '||'. 
                        If a compoundNode is right before '&&' ('||'), then the 
                        simult of all the commands in its tails is merged into 
                        the simult of current CommandNode. 


        Let me explain how to add tails and precursors. 
        1) tails. 
            If it's a CommandNode, the tails only contains itself. 
            If it's an IfNode, then tails contains the tails of the last command in each condition and body lists. 
            If it's a WhileNode, the tails contains the tails of the last command in condition and body lists. 
            If it's a ForNode, the tails contains the tails of the last command in the body. 
            The last command of a list is defined as follows. 
            (1) last command of If condition is followed by a ReservedNode('then')
            (2) last command of If body is followed by a ReservedNode('elif'), 'else', or 'fi'.
            (3) last command of while condition is followed by a ReservedNode('do) 
            (4) last command of while body is followed by a ReservedNode('done')
            (5) last command of for body is followed by a ReservedNode('done')
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
            (1) ReservedNode
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
        self.tails = []
        self.precursors = []
        self.simult = []
        self.pre = None


class Node(object):

    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

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


class TreeVisitor:
    def __init__(self, tree):
        self.tree = tree
        self.if_stack = []
        self.while_stack = []
        self.current_path_to_root = []

    """
        Set tails of node and 
        Set precursors and tails of its children
    """
    def recursive_visit(node):
        kind = node.data.kind
        if "ReservedNode" == kind or "ParameterNode" == kind or 
            "OperatorNode" == kind or "RedirectNode" == kind or
            "PipeNode" == kind:
            return
        #
        #   Todo: handle "||" and "&&" operation
        #
        if "ListNode" == kind or "CompundNode" == kind:
            # set precursors of each command children
            # make tails for each command children
            first_command_child = True
            last_command_child = None
            for i in range(len(node.children)):
                # It's a command node
                if node.children[i].data.kind != "ReservedNode" and 
                    node.children[i].data.kind != "ParameterNode" and 
                    node.children[i].data.kind != "OperatorNode" and
                    node.children[i].data.kind != "RedirectNode" and
                    node.children[i].data.kind != "PipeNode": 
                    if node.children[i].data.kind == "WordNode" and
                       len(node.children[i].children) > 1:
                        # first command node
                        if True == first_command_child:
                            first_command_child = False
                            node.children[i].data.precursors = node.data.precursors
                        # other command node
                        else:
                            node.children[i].data.precursors = last_command_child.data.tails
                            node.children[i].data.pre = last_command_child
                        # recursively set tails for this command
                        # recursively set precursors and tails of its children
                        self.current_path_to_root.append(node.children[i])
                        self.recursive_visit(node.children[i])
                        self.current_path_to_root.pop(node.children[i])
                        last_command_child = node.children[i]

            # --- make tails for the node itself
            node.data.tails = last_command_child.data.tails

        elif "WordNode" == kind or "AssignmentNode" == kind:
            # substitution and parameter are the only cases
            if len(node.children) > 0:
                # set precursors of each command children
                # make tails for each command children
                first_command_child = True
                last_command_child = None
                for i in range(len(node.children)):
                    if node.children[i].data.kind == "CommandsubstitutionNode":
                        if True == first_command_child:
                            first_command_child = False
                            node.children[i].data.precursors = node.data.precursors
                        else:
                            node.children[i].data.precursors = last_command_child.data.tails
                            node.children[i].data.pre = last_command_child
                        # recursively set tails for this command
                        # recursively set precursors and tails of its children
                        self.current_path_to_root.append(node.children[i])
                        self.recursive_visit(node.children[i])
                        self.current_path_to_root.pop(node.children[i])
                        last_command_child = node.children[i]
                    else:
                        print("%s: illegal children:%s" % (node.data.kind, node.children[i].data.kind))
                        exit(1)
                node.data.tails = last_command_child.data.tails
            # its a leaf, set a safe guard
            else:
                node.data.tails = None

        elif "IfNode" == kind:
            pass 
        elif "WhileNode" == kind:
            pass

        elif "ForNode" == kind:
            pass
        elif "CommandNode" == kind:
            pass
        elif "CommandsubstitutionNode" == kind:
            pass
        elif "PipelineNode" == kind:
            pass

        else:
            print("Unknown kind:%s" % kind)
            exit(2)





    def make_last_commands(self, node):
        if len(node.children) > 0:
            child = node.children[-1]
            command = self.get_last_command(child)
        else: 

'''
    The key idea is to parse the .out file line by line. 
    Then we get a hierarchical structure like this: 

    IfNode(
        ReservedwordNode('if')
        ListNode(
            CommandNode('[...]')
            OperatorNode(';')
        )
        ReservedNode('then')
        ListNode(
            CommandNode('...')
            OperatorNode(';)
            CommandNode('...')
            OperatorNode('\n')
        )
        ReservedNode('elif')
        ListNode(
            CommandNode('...')
            OperatorNode('\n')
            CommandNode('...')
            OperatorNode('\n')
        )
        ReservedNode('then)
        ListNode(
            CommandNode('...')
            OperatorNode('\n')
            CommandNode('...')
            OperatorNode('\n')
        )
        ReservedNode('else')
        ListNode(
            CommandNode('...')
            OperatorNode('\n')
            CommandNode('...')
            OpeartorNode(';')
        )
        ReservedNode('fi')
    )

    To be simple, lets denote it as follows. 

    IfNode
        ReservedNode(if)
        ListNode(condition1)
            CommandNode(1)
            CommandNode(2)
        ReservedNode(then)
        ListNode(body1)
            CommandNode(3)
            CommandNode(4)
        ReservedNode(elif)
        ListNode(condition2)
            CommandNode(5)
            CommandNode(6)
        ReservedNode(then)
        ListNode(body2)
            CommandNode(7)
            CommandNode(8)
        ReservedNode(else)
        ListNode(body3)
            CommandNode(9)
            CommandNode(10)
        ReservedNode(fi)


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

    (1): The command immediate after ReservedNode('if') is the 
    first command of IfNode. 

    (2): For commands within the same IfNode, the rules are as follows.
    
    1) If a node is in the condition, then its precursor must be the following. 
        + Condition lists before this condition. 

    2) If a node is in the body, then its precursor must be one of the following. 
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

'''
Assumption: 
    CommandNode is the basic representation of a "command".
    But there are some exceptions. 

'''


    def get_last_commands(self, node):
        last_commands = None
        if ("CommandNode" == node.data.kind):
            last_commands = self.make_last_command(node)
        elif ("IfNode" == node.data.kind):
            last_commands = self.make_last_if_commands(node)
        elif ("While")
        else: 
            if len(node.children) > 0:
                last_commands = self.get_last_commands(node.children[-1])
        return last_commands


    def visit_node(self, node):
        self.pre_visit(node)
        if len(node.children) < 1:
            self.process_node(node)
        self.post_visit(node)
        
    def process_node(self, node):
        pass



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
            line = fp.readline()
    #tree.dump_leaves(tree.root)
    #tree.dump_commands(tree.root)
    tree.update_command_connectors()
    node_list = tree.dump_command_connectors()
    print_graph(node_list)
    #print(tree.commands)