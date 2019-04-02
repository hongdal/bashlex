import os

class mappting_table:

    def __init__(self):
        # the path of the cmd to syscall mapping files. 
        self.fpath = ""
        self.cmd2syscall = {}

    # Load cmd to syscall table from file. 
    # fpath :   the path of the dir storing all mappings. 
    # return:   the hash table of tha cmd2syscall mapping. 
    #           key: string of cmd, value: list of mapping. 
    def load_map(self, fpath):
        for filename in os.listdir(fpath):
            cmd = filename[:-4]
            file = open(fpath+filename, 'r') 
            syscalls = file.read().split()
            self.cmd2syscall[cmd] = syscalls
        return self.cmd2syscall

    # Ask for the syscall sequence of a command. 
    # cmd   :   the command. 
    # return:   a list of string, each string is a name of syscall. 
    def get_syscall(self, cmd):
        if cmd not in self.cmd2syscall:
            return False
        return self.cmd2syscall[cmd]