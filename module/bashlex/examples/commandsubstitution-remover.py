import sys
import argparse
from argparse import RawTextHelpFormatter
from bashlex import parser, ast


class nodevisitor(ast.nodevisitor):
    def __init__(self, positions):
        self.positions = positions

    def visitcommandsubstitution(self, n, command):
        # log the start and end positions of this command substitution
        self.positions.append(n.pos)

        # do not recurse into child nodes
        return False


desc = '''replace all occurrences of $() and `` with the string given in -s

  $ commandsubstitution-remover.py -s nope -c 'foo $(bar)'
  foo nope

within words:

  $ commandsubstitution-remover.py -c '"foo $(bar) baz"'
  "foo XXX baz"

but not within single quotes, since codhey cancel special meaning:

  $ commandsubstitution-remover.py -c "foo '"'$(bar)'"'"
  foo '$(bar)'

(this a simple script to demonstrate how to traverse the ast produced
by bashlex)
'''

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description=desc,
                                        formatter_class=RawTextHelpFormatter)
    argparser.add_argument('-s', dest='replacement', metavar='S', default='XXX',
                           help='replace occurrences with S (default: XXX)')

    group = argparser.add_mutually_exclusive_group()
    group.add_argument('file', metavar='file', type=file, nargs='?',
                       help='file to parse')
    group.add_argument('-c', dest='expression',
                       help='string to parse')

    args = argparser.parse_args()

    if args.expression:
        s = args.expression
    elif args.file:
        s = args.file.read()
        # Read the Bash scripts from a file.
    else:
        s = sys.stdin.read()

    # From Bashlex import parse
    trees = parser.parse(s, False)
    positions = []
    # This Trees[1] is works for the command.
    # print trees[0]
    for tree in trees:
        # print tree[0]
        print(tree.dump())
        visitor = nodevisitor(positions)
        visitor.visit(tree)

    # do replacements from the end so the indicies will be correct
    # positions.reverse()

    # postprocessed = list(s)

    # for start, end in positions:
    #     # replace the portion of the input where the substitution occurred
    #     # with the replacement string
    #     postprocessed[start:end] = args.replacement

    # print ''.join(postprocessed)
