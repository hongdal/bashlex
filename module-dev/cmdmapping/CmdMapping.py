import netnode as nn 
import mapping_table as mt 
import sys


path_generator_status = [
    "none",
    "refreshed"
]


class CmdMapping:

    def __init__(self):
        self.mapping_table = mt.mappting_table()
        self.path_generator_status = "none"


    # Input: the path of the folder containing the files of mapping table. 
    def load_mapping_table(self, fpath):
        self.mapping_table.load_map(fpath)


    # Each time we want to load a new bash graph (.dot file), we need 
    # a new path_generator
    def refresh_path_generator(self, fname):
        self.path_generator = nn.netnodex()
        self.path_generator.read_from_dot(fname)
        self.path_generator.load_node_names()
        sys.stderr.write("May take a while ...\n")
        self.path_generator.get_start_to_end_paths()
        self.path_generator.condense_all_paths()
        sys.stderr.write("Paths generated!!\n")
        self.path_generator_status = "refreshed"


    # shortest  :   the shortest length of path want to return 
    # longest   :   the longest length of the path want to return.
    # return    :   a list of list of string
    def get_cmd_paths(self, shortest, longest):
        if self.path_generator_status != "refreshed":
            sys.stderr.write("Please run refresh_path_generator() first.\n")        
            return False 
        # This gives back a set of tuple, each tuple is a path. 
        set_tuple_paths = self.path_generator.get_path_with_length(shortest, longest)
        ret = []
        for path in set_tuple_paths:
            list_path = []
            for cmd in path:
                cmd = cmd.replace(r'"', r'')
                cmd = cmd.replace(r'', r'')
                list_path.append(cmd)
            ret.append(list_path)
        return ret
    
    
    # path     :   A list of string
    # Returh a single path in system call level. 
    # It's a list of list. 
    # E.g., [['open', 'write'], ['open', 'read']...]
    def get_syscall_path(self, path):
        # ret is a list of list of string
        ret = []
        # for each element in the tuple
        for cmd in path:
            # syscalls is a list of string. 
            syscalls = self.mapping_table.get_syscall(cmd)
            if False != syscalls:
                ret.append(syscalls)
            else:
                if 'BINARY_COMMAND' != cmd:
                    sys.stderr.write('Unknwon command: ' + cmd + '\n')
        return ret


    # The same as get_cmd_paths except that it returns the paths in 
    # system call level. 
    def get_syscall_paths(self, shortest, longest):
        if self.path_generator_status != "refreshed":
            sys.stderr.write("Please run refresh_path_generator() first.\n")        
            return False 
        # Gives back a list of list of string
        paths = self.get_cmd_paths(shortest, longest)
        syscall_paths = []
        # path is a list of string
        for path in paths:
            # syscall_path is a list of list of string
            syscall_path = self.get_syscall_path(path)
            syscall_paths.append(syscall_path)
        return syscall_paths

    # path  :   the path to dump, a list of string
    # encode:   print number if True, print raw string if False. 
    def dump_path(self, path, encode=True):
        if encode:
            path = self.mapping_table.encode_path(path)
        self.mapping_table.dump_path(path)