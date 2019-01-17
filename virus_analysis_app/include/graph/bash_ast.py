
class NodeData(object):

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

