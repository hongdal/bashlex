#!/usr/bin/env python3
# coding=utf-8

import re
regex = r"([a-zA-Z]+)(Node)"


def parse_none(line, indent):
    pass


def parse_node(line, kind, indent):
    if "WordNode" == kind:
        data = NodeData(int(indent)/2, kind, kind)
        


if __name__ == "__main__": 
    with open("./testcase/2.out") as fp:
        line = fp.readline()
        count = 1
        while line:
            # Count leading space
            lspace = len(line) - len(line.lstrip())
            # Search for the node type. 
            node = re.search(regex, line)
            if None != node:
                print("%d, %s" % (lspace, node.group(0)))
            line = fp.readline()


