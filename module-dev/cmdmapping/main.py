import CmdMapping as cm  



if __name__ == "__main__":
    mapper = cm.CmdMapping()
    mapper.load_mapping_table("cmd2syscall/")
    mapper.refresh_path_generator("mediaset/100.dot")
    cmd_paths = mapper.get_cmd_paths(0, 100)
    syscall_paths = mapper.get_syscall_paths(0, 100)
    exit(0)
    for syscall_path in syscall_paths:
        path = []
        for cmd in syscall_path:
            path.extend(cmd)
        print(path)