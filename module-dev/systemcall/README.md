# How to use the strace command

**1. Run application by strace**

```bash
strace -tt -T -f -p 28824
```


**2. Monitor the PID for application**

```bash
strace -ttt -T -f -o /temp/strace.log 1024 ./bashscript
```

strace -e trace=open,read -p 22254 -s 80 -o debug.webserver.txt

If you only want to see a few files.

```bash
-e trace=set 
-e trace=file 
-e trace=process 
-e trace=network 
-e trace=signal 
-e trace=ipc 
-e trace=desc 
-e trace=memory 
-e abbrev=set 
-e verbose=set
```

-tt 在每行输出的前面，显示毫秒级别的时间
-T 显示每次系统调用所花费的时间
-v 对于某些相关调用，把完整的环境变量，文件stat结构等打出来。
-f 跟踪目标进程，以及目标进程创建的所有子进程
-e 控制要跟踪的事件和跟踪行为,比如指定要跟踪的系统调用名称
-o 把strace的输出单独写到指定的文件
-s 当系统调用的某个参数是字符串时，最多输出指定长度的内容，默认是32个字节
-p 指定要跟踪的进程pid, 要同时跟踪多个pid, 重复多次-p选项即可。


Check all process now.

`strace -p $(pgrep command) -o file.out`

strace bash -c 'cd /path/to/destination/'
{ strace -p "$$" & sleep 1; cd /some/dir; kill "$!"; }


systemtap, oprofile

您可以使用Linux内核审计子系统。

例如，要查看名为sshd（pid - 12345）的程序所做的所有系统调用：

# auditctl -a entry,always -S all -F pid=12345



# Some links

**Strace**

* https://github.com/jessfraz/strace2elastic
* https://github.com/brendangregg/perf-tools
* Maybe: auditd: https://security.stackexchange.com/questions/8485/monitoring-system-calls-in-a-reliable-and-secure-way