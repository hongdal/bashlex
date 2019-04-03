import os

'''
This class loads the mapping table from a folder. 
Then it stores the mapping table in memory. 
In addition, it encodes each system call as a number. 

'''

class mappting_table:

    def __init__(self):
        # the path of the cmd to syscall mapping files. 
        self.fpath = ""
        self.cmd2syscall = {}
        self.syscall2num = {}
        self.num2syscall = {}


    def encode_table(self):
        syscalls = set()
        for cmd in self.cmd2syscall:
            for syscall in self.cmd2syscall[cmd]:
                syscalls.add(syscall)
        sorting = list(syscalls)
        sorting.sort()
        index = 1
        self.syscall2num = {}
        self.num2syscall = {}
        for syscall in sorting:
            self.syscall2num[syscall] = index
            self.num2syscall[index] = syscall
            index += 1


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
        self.encode_table()
        return self.cmd2syscall

    # Ask for the syscall sequence of a command. 
    # cmd   :   the command. 
    # return:   a list of string, each string is a name of syscall. 
    def get_syscall(self, cmd):
        if cmd not in self.cmd2syscall:
            return False
        return self.cmd2syscall[cmd]


    # Input :   a syscall 
    # return:   a number
    def encode_syscall(self, syscall):
        if syscall in self.syscall2num:
            return self.syscall2num[syscall]
        else:
            return False


    # Input :   a number
    # return:   a syscall
    def decode_syscall(self, num):
        if num in self.num2syscall:
            return self.num2syscall[num]
        else:
            return False

    # Input :   a list of syscalls. 
    # return:   a list of numbers
    # Note:     unknown syscall translates to 0
    def encode_path(self, path):
        ret = []
        for syscall in path:
            val = self.encode_syscall(syscall)
            if False != val:
                ret.append(val)
            else:
                ret.append(0)
        return ret


    # Input :   a list of numbers.
    # return:   a list of syscalls
    # Note:     unknown number translates to "unknown"
    def decode_path(self, path):
        ret = []
        for num in path:
            val = self.decode_syscall(num)
            if False != val:
                ret.append(val)
            else:
                ret.append("unknown")
        return ret

    # Input :   a list of numbers/syscalls 
    # Note  :   this method prints the path to standard output in a line. 
    def dump_path(self, path):
        outstring = ""
        for element in path:
            outstring += str(element) + ","
        outstring = outstring[:-1]
        print(outstring)
