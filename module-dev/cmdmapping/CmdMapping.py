import netnode as nn 
import mapping_table as mt 


path_generator_status = [
    "none",
    "refreshed"
]


class CmdMapping:

    def __init__(self):
        self.mapping_table = mt.mappting_table()
        self.path_generator_status = "none"


    def load_mapping_table(self, fpath):
        self.mapping_table.load_map(fpath)


    # Each time we want to load a new bash graph, we need 
    # a new path_generator
    def refresh_path_generator(self, fname):
        self.path_generator = nn.netnodex()
        self.path_generator.read_from_dot(fname)
        self.path_generator.load_node_names()
        print("May take a while ... ")
        self.path_generator.get_start_to_end_paths()
        self.path_generator.condense_all_paths()
        print("Paths generated!!")
        self.path_generator_status = "refreshed"


    def get_cmd_paths(self, shortest, longest):
        if self.path_generator_status != "refreshed":
            print("Please run refresh_path_generator() first.")        
            return False 
        return self.path_generator.get_path_with_length(shortest, longest)


    def get_syscall_paths(self, shortest, longest):
        if self.path_generator_status != "refreshed":
            print("Please run refresh_path_generator() first.")        
            return False 
        paths = self.get_cmd_paths(shortest, longest)
        # this is a list of list of list
        # Most inner list: a list of syscall for a single command. 
        # second inner list: a list of command for a path. 
        # Most outter list: a list of path
        syscall_paths = []
        for path in paths:
            # syscall_path is a list of list
            syscall_path = self.get_syscall_path(path)
            syscall_paths.append(syscall_path)
        return syscall_paths


    def get_syscall_path(self, path):
        # ret is a list of list. 
        ret = []
        for cmd in path:
            # syscalls is a list of string. 
            syscalls = self.mapping_table.get_syscall(cmd)
            ret.append(syscalls)
        return ret


