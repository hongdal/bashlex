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



No. | Linux Command | Frequency | Classification        | Number of Files
----|---------------|-----------|-----------------------|----------------
1   | ~~cd~~            | 109306    | directories           | 1715
2   | ~~chmod~~         | 22237     | file permissions      | 1727
3   | ~~rm~~            | 15666     | file operations       | 1215
4   | ~~wget~~          | 15491     | network               | 1214
5   | ~~cat~~           | 6767      | file examination      | 537
6   | tftp          | 6445      | network               | 503
7   | ~~curl~~          | 2306      | network               | 199
8   | ~~ulimit~~        | 515       | miscellaneous         | 514
9   | ~~cp~~            | 507       | file operations       | 503
10  | ~~echo~~          | 244       | shell scripting       | 33
11  | ~~grep~~          | 157       | searching and sorting | 19
12  | pkill         | 103       | process management    | 3
13  | ~~awk~~           | 69        | Text processing       | 12
14  | ~~sudo~~          | 65        | users and groups      | 12
15  | killall       | 56        | process management    | 5
16  | xargs         | 53        | searching and sorting | 8
17  | ~~ps~~            | 53        | process management    | 8
18  | ~~sleep~~         | 42        | miscellaneous         | 20
19  | ~~exit~~          | 29        | basic shell           | 16
20  | nohup         | 25        | process management    | 10
21  | service       | 24        | Others                | 22
22  | mktemp        | 16        | filesystem            | 4
23  | sed           | 15        | regular expressions   | 9
24  | set           | 14        | shell scripting       | 2
25  | lynx          | 13        | network               | 1
26  | cut           | 13        | Shell Programming     | 5
27  | ~~apt-get~~       | 13        | Others                | 7
28  | ~~wc~~            | 12        | file examination      | 6
29  | ~~tr~~            | 11        | Text processing       | 6
30  | ~~mkdir~~         | 10        | directories           | 8
31  | tail          | 9         | file examination      | 5
32  | declare       | 9         | Others                | 1
33  | basename      | 9         | filesystem            | 4
34  | lsof          | 8         | filesystem            | 2
35  | read          | 7         | shell scripting       | 3
36  | yum           | 6         | Others                | 4
37  | tar           | 6         | compression           | 6
38  | crontab       | 6         | miscellaneous         | 3
39  | perl          | 5         | programming           | 3
40  | usermod       | 4         | Others                | 4
41  | sort          | 4         | searching and sorting | 4
42  | mv            | 4         | file operations       | 2
43  | head          | 4         | file examination      | 3
44  | whoami        | 3         | users and groups      | 2
45  | uname         | 3         | system information    | 3
46  | touch         | 3         | file operations       | 2
47  | ls            | 3         | directories           | 3
48  | find          | 3         | searching and sorting | 3
49  | chattr        | 3         | Others                | 1
50  | which         | 2         | searching and sorting | 2
51  | unset         | 2         | shell scripting       | 2
52  | ~~umask~~         | 2         | file permissions      | 2
53  | sysctl        | 2         | Others                | 2
54  | stat          | 2         | Others                | 1
55  | ~~ping~~          | 2         | network               | 2
56  | netstat       | 2         | network               | 2
57  | lsb_release   | 2         | Others                | 2
58  | kill          | 2         | process management    | 2
59  | ~~ip~~            | 2         | network               | 2
60  | ~~ifconfig~~      | 2         | network               | 1
61  | ~~id~~          | 2         | Others                | 2
62  | ~~history~~       | 2         | basic shell           | 2
63  | gunzip        | 2         | compression           | 2
64  | export        | 2         | shell scripting       | 1
65  | ~~date~~          | 2         | system information    | 2
66  | uniq          | 1         | searching and sorting | 1
67  | trap          | 1         | process management    | 1
68  | test          | 1         | Others                | 1
69  | su            | 1         | users and groups      | 1
70  | sh            | 1         | Shell programming     | 1
71  | nc            | 1         | network               | 1
72  | make          | 1         | build management      | 1
73  | git           | 1         | build management      | 1
74  | expr          | 1         | Others                | 1
75  | egrep         | 1         | regular expressions   | 1
76  | dirname       | 1         | filesystem            | 1
77  | clear         | 1         | basic shell           | 1
78  | chown         | 1         | file permissions      | 1
79  | arp           | 1         | network               | 1