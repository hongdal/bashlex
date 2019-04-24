import json

class Automaton:

    def __init__(self):
        self.cfg = None
        self.edges = {}
        self.dependencies = {}
        self.cmd2capability = None 
        self.capability2cmd = None


    '''
        The file refered by `filename` is a json file. It looks like this:
        {
            FP  :   [cd],
            DW  :   [wget, ftp, tftp], 
            ...
        }

        The self.capability2cmd looks like this:
        {
            FP  :   {cd},
            DW  :   {wget, ftp, tftp},
            ...
        }

        The self.cmd2capability looks like this:
        {
            cd      :   {FP},
            wget    :   {DW},
            cat     :   {CW, CP},
            ...
        }
    '''
    def load_capabilities(self, filename):
        with open(filename, 'r') as infile:
            data = json.loads(infile.read())
        self.capability2cmd = {}
        self.cmd2capability = {}
        for capability, commands in data.items():
            # load capability2cmd
            self.capability2cmd[capability] = set(commands) 
            # load cmd2capability
            for cmd in commands:
                if cmd not in self.cmd2capability:
                    self.cmd2capability[cmd] = set([capability])
                else:
                    self.cmd2capability[cmd].add(capability)


    '''
        This method updates the automaton using a given CFG.
        Input:  A cfg returned by BashGraph.get_graph()
        The CFG looks like this:

        {
            cd : [cd, wget],
            wget: [chmod, cat, rm],
            chmod: [rm],
            ...
        }

        The key for each record is a command.
        The value for each record is a list of commands following that command in the key.
    '''
    def update_with_cfg(self, cfg):
        if None == self.capability2cmd:
            print("Capability table not loaded, please call 'load_capabilities' first. ")
            return False
        self.cfg = cfg
        self.update_edges()
        self.update_dependencies()
        self.update_automaton()
        return self.automaton


    '''
        The self.edges is a dictionary like this:
        {
            (cd,wget) : 3,
            (wget,chmod) : 1,
            ...
        }

        The key of each record is a tuple indicating the two consective commands.
        The value of each record is a number indicating how many occurence of that. 
    '''    
    def update_edges(self):
        edges = {}
        for key in self.cfg.keys():
            for node in self.cfg[key]:
                edge = (key.data.label, node.data.label)
                if edge in edges:
                    edges[edge] += 1
                else:
                    edges[edge] = 1
        for key, value in edges.items():
            if key in self.edges:
                self.edges[key] += value 
            else:
                self.edges[key] = value
        return self.edges


    '''
        This method must be called after self.update_edges

        TODO:   In the case where a command maps to mutiple capabilities, this 
        dependency algorithm does not work well. It cannot assign the weights 
        seperately. Because at this time, we cannot determine the command will 
        cause which transistion. E.g., 
        cat -> service can be interpretered as any one of the following:
        CW -> KILL
        CW -> EXE
        CP -> KILL
        CP -> EXE
        By only looking at the two commands (i.e., `cat` and `service`), we cannot 
        determine which case it belongs to. 
        What we do now is to assign the same value for all the cases. 

        Note: the self.dependencies is the same as an automaton right now. But I design 
        this function for future extension. 

        The self.dpendencies is a dictionary like this:
        {
            FP  :   {
                DW  :   {wget : 3}
                CH  :   {},
                ...
            }, 
            DW  :   {
                FP  :   {},
                CH  :   {chmod : 1},
                CP  :   {cp : 2, cat : 5, echo : 2}
                ...
            }
        }

        This is a dictionary of dictionary of dictionary.
        The outter dictionary has the key of each `source` capability.
        The middle dictionary has the key of a `target` capability.
        The inner dictionary has the key of a command as the edge betwen `source` and `target` capabilities.
        The value of inner dictionary has the value of weight of the transition.
        E.g., in the above dictionary, 
          There is an edge from FP to DW, with weight 3.
          There is no edge from FP to CH. 

    '''
    def update_dependencies(self):
        # Totally reconstruct
        self.dependencies = {}
        # for each edge
        for key, value in self.edges.items():
            sources = self.comamnd_to_capabilities(key[0])
            dests = self.comamnd_to_capabilities(key[1])
            # Iterate through all sources and dests of this edge.
            for source in sources:
                for dst in dests:
                    if source not in self.dependencies:
                        self.dependencies[source] = {}
                        self.dependencies[source][dst] = {}
                        self.dependencies[source][dst][key[1]] = value
                    elif dst not in self.dependencies[source]:
                        self.dependencies[source][dst] = {}
                        self.dependencies[source][dst][key[1]] = value
                    elif key[1] not in self.dependencies[source][dst]:
                        self.dependencies[source][dst][key[1]] = value
                    else:
                        self.dependencies[source][dst][key[1]] += value
        return self.dependencies


    '''
        Returns a set of commands given a capability
    '''  
    def capability_to_commands(self, capability):
        if capability in self.capability2cmd:
            return self.capability2cmd[capability]
        else:
            return set(["UNKNOWN"])


    '''
        Returns a set of capabilities given a command
    '''
    def comamnd_to_capabilities(self, command):
        if command in self.cmd2capability:
            return  self.cmd2capability[command]
        else:
            return set(["UNKNOWN"])


    '''
        This method must be called after self.update_dependencies

        The key of each record is a tuple indicating the two consective capabilities.
        The value of each record is a number indicating how many occurence of that. 

        The self.automaton looks like this:
        {
            FP  :   {
                DW  :   {wget : 3}
                CH  :   {},
                ...
            }, 
            DW  :   {
                FP  :   {},
                CH  :   {chmod : 1},
                CP  :   {cp : 2, cat : 5, echo : 2}
                ...
            }
        }
        This is a dictionary of dictionary of dictionary.
        The outter dictionary has the key of each `source` capability.
        The middle dictionary has the key of a `target` capability.
        The inner dictionary has the key of a command as the edge betwen `source` and `target` capabilities.
        The value of inner dictionary has the value of weight of the transition.
        E.g., in the above dictionary, 
          There is an edge from FP to DW, with weight 3.
          There is no edge from FP to CH. 

    '''
    def update_automaton(self):
        self.automaton = self.dependencies


    def print_automaton(self):
        print("digraph {")
        for source in self.automaton:
            for dst in self.automaton[source]:
                edges = self.automaton[source][dst]
                for edge in edges:
                    edge_name = edge 
                    edge_weight = edges[edge] 
                    edge_label = '[label = ' + '"' + edge_name + ':' + str(edge_weight) + '"]'
                    connection = source + ' -> ' + dst + ' ' + edge_label + ';'
                    print(connection)
        print("}")