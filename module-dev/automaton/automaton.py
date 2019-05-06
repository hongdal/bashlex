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
        cause which transition. E.g., 
        `cat -> service` can be interpretered as any one of the following:
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
                SAFE:   {cd : 0, rm : 0, ... }  // all other commands go here, the weight is zero. This field is not necessary. If we add 0 to the score when we get here.
                ...
            }, 
            DW  :   {
                FP  :   {},
                CH  :   {chmod : 1},
                CP  :   {cp : 2, cat : 5, echo : 2},
                SAFE:   {cd : 0, rm : 0, ... }  // all other commands go here, the weight is zero. This field is not necessary. If we add 0 to the score when we get here.
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

    ''' 
        This function computes and returns a score of a given sequence. 
        The algorithm is as follows. 

        1. Iterate the commands in the path. 
        2. transit according to the path. 
        3. Record the target state. 
            If the target state is "safe", add 0 to the score.
            If the target state is any other state, add corresponding weight to the score. 
            
        path:  a list of sequence
        return: a real number
    '''
    def get_score(self, path):
        pass


    '''
        This function dumps an automaton as a tuple-value dictionary and returns the dictionary.
        E.g., an automaton like this: 
        {
            FP  :   {
                DW  :   {wget : 3}
                CH  :   {},
                SAFE:   {cd : 0, rm : 0, ... }  // all other commands go here, the weight is zero. This field is not necessary. If we add 0 to the score when we get here.
                ...
            }, 
            DW  :   {
                FP  :   {},
                CH  :   {chmod : 1},
                CP  :   {cp : 2, cat : 5, echo : 2},
                SAFE:   {cd : 0, rm : 0, ... }  // all other commands go here, the weight is zero. This field is not necessary. If we add 0 to the score when we get here.
                ...
            }
        }

        The dumped automaton will be like this:
        {
            (FP, DW, wget)  :   3,
            (FP, SAFE, cd)  :   0,
            (FP, SAFE, rm)  :   0,
            (DW, CH, chmod) :   1, 
            (DW, CP, cp)    :   2,
            (DW, CP, cat)   :   5,
            (DW, CP, echo)  :   2,
            ...
        }

    '''
    def encode_automaton(self):
        self.encoded_automaton = {}
        for src, dsts in self.automaton.items():
            for dst, edges in dsts.items():
                for edge, weight in edges.items():
                    transition = (src, dst, edge)
                    self.encoded_automaton[transition] = weight
        return self.encoded_automaton


    '''
        data    :   a dictionary, which is an encoded automaton
        return  :   a decoded automaton. 
        The internal self.automaton is updated accordingly. 
    '''
    def decode_automaton(self, data):
        self.automaton = {}
        for key, weight in self.automaton.items():
            src = key[0]
            dst = key[1]
            edge = key[2] 
            if src not in self.automaton:
                self.automaton[src] = {}
            if dst not in self.automaton[src]:
                self.automaton[src] = {}
            self.automaton[src][dst][edge] = weight
        return self.automaton


    '''
        This writes an automaton to a file json file.
        fpath   :   the path to the json file. 
        return  :   True if successful, False if fail
    '''
    def write_automaton_to_file(self, fpath):
        if None != self.automaton:
            with open(fpath, 'w') as outfile:
                json.dump(self.automaton, outfile)
            return True
        else:
            return False


    '''
        This function should be always successful. 
        It updates self.automaton accordingly. 
        fpath   :   the file path of json file. 
        return  :   self.automaton 

    '''
    def read_automaton_from_file(self, fpath):
        with open(fpath, 'r') as infile:
            self.automaton = json.load(infile)
        return self.automaton


    '''
        Print the automaton to a .dot file. 
        The .dot file then can be visualized by graphviz tool. 
    '''
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


    def print_edges(self):
        for key in self.edges:
            print(key)

