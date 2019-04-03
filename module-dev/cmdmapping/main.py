import CmdMapping as cm  
import os
import sys

#fpath="/home/hongda/Dropbox/Github/virus_analysis/module-dev/cmdmapping/mediaset/"
fpath="/home/hongda/GitHub-offbox/virus_analysis/module-dev/all-cd-commands/"

if __name__ == "__main__":
    mapper = cm.CmdMapping()
    mapper.load_mapping_table("cmd2syscall/")
    for filename in os.listdir(fpath):
        sys.stderr.write(filename + fpath + '\n')
        mapper.refresh_path_generator(fpath + filename)
        cmd_paths = mapper.get_cmd_paths(0, 100)
        syscall_paths = mapper.get_syscall_paths(0, 100)
        for syscall_path in syscall_paths:
            path = []
            for cmd in syscall_path:
                path.extend(cmd)
            mapper.dump_path(path)