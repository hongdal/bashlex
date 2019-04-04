#!/usr/bin/env python
# coding=utf-8


ret = ""
with open("./patterns.dat") as infile:
    line = infile.readline()
    line = line.rstrip("\r\n")
    ret += line
    while line:
        line = infile.readline() 
        if line :
            line = line.rstrip("\r\n")
            ret += "," + line

print ret

