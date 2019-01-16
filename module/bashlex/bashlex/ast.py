from copy import copy

class node(object):
    """
    This class represents a node in the AST built while parsing command lines.
    It's basically an object container for various attributes, with a slightly
    specialised representation to make it a little easier to debug the parser.
    """

    def __init__(self, **kwargs):
        assert 'kind' in kwargs
        self.__dict__.update(kwargs)

    # The Last part: Add indent for each part
    def dump(self, indent='  '):
        return _dump(self, indent)

    def __repr__(self):
        chunks = []
        d = dict(self.__dict__)
        kind = d.pop('kind')
        for k, v in sorted(d.items()):
            chunks.append('%s=%r' % (k, v))
        return '%sNode(%s)' % (kind.title(), ' '.join(chunks))

    def __eq__(self, other):
        if not isinstance(other, node):
            return False
        self_dict = copy(self.__dict__)
        other_dict = copy(other.__dict__)
        for wrd in ["lineno", "discard"]:
            self_dict.pop(wrd, None)
            other_dict.pop(wrd, None)
        return self_dict == other_dict

class nodevisitor(object):
    def _visitnode(self, n, *args, **kwargs):
        k = n.kind
        self.visitnode(n)
        return getattr(self, 'visit%s' % k)(n, *args, **kwargs)

    def visit(self, n):
        k = n.kind
        if k == 'newline':
            self._visitnode(n)
        elif k == 'pattern':
            dochild = self._visitnode(n, n.pattern, n.actions)
            if dochild is None or dochild:
                for child in n.pattern:
                    self.visit(child)
                for child in n.actions:
                    self.visit(child)
        elif k == 'operator':
            self._visitnode(n, n.op)
        elif k == 'list':
            dochild = self._visitnode(n, n.parts)
            if dochild is None or dochild:
                for child in n.parts:
                    self.visit(child)
        elif k == 'reservedword':
            self._visitnode(n, n.word)
        elif k == 'pipe':
            self._visitnode(n, n.pipe)
        elif k == 'pipeline':
            dochild = self._visitnode(n, n.parts)
            if dochild is None or dochild:
                for child in n.parts:
                    self.visit(child)
        elif k == 'compound':
            dochild = self._visitnode(n, n.list, n.redirects)
            if dochild is None or dochild:
                for child in n.list:
                    self.visit(child)
                for child in n.redirects:
                    self.visit(child)
        elif k in ('if', 'for', 'while', 'until'):
            dochild = self._visitnode(n, n.parts)
            if dochild is None or dochild:
                for child in n.parts:
                    self.visit(child)
        elif k == 'case':
            dochild = self._visitnode(n, n.parts)
            if dochild is None or dochild:
                for child in n.parts:
                    self.visit(child)
        elif k == 'command':
            self.correct_heredoc_lineno(n)
            dochild = self._visitnode(n, n.parts)
            if dochild is None or dochild:
                for child in n.parts:
                    self.visit(child)
        elif k == 'function':
            dochild = self._visitnode(n, n.name, n.body, n.parts)
            if dochild is None or dochild:
                for child in n.parts:
                    self.visit(child)
        elif k == 'redirect':
            dochild = self._visitnode(n, n.input, n.type, n.output, n.heredoc)
            if dochild is None or dochild:
                if isinstance(n.output, node):
                    self.visit(n.output)
                if n.heredoc:
                    self.visit(n.heredoc)
        elif k in ('word', 'assignment'):
            dochild = self._visitnode(n, n.word)
            if dochild is None or dochild:
                for child in n.parts:
                    self.visit(child)
        elif k in ('parameter', 'tilde', 'heredoc'):
            self._visitnode(n, n.value)
        elif k in ('commandsubstitution', 'processsubstitution'):
            dochild = self._visitnode(n, n.command)
            if dochild is None or dochild:
                self.visit(n.command)
        else:
            raise ValueError('unknown node kind %r' % k)
        self.visitnodeend(n)

    def correct_heredoc_lineno(self, node):
        for part in node.parts:
            if part.kind == 'redirect' and part.heredoc:
                node.lineno = part.heredoc.lineno + 1

    def visitnode(self, n):
        pass
    def visitnewline(self, n):
        pass
    def visitpattern(self, n, pattern, actions):
        pass
    def visitnodeend(self, n):
        pass
    def visitoperator(self, n, op):
        pass
    def visitlist(self, n, parts):
        pass
    def visitpipe(self, n, pipe):
        pass
    def visitpipeline(self, n, parts):
        pass
    def visitcompound(self, n, list, redirects):
        pass
    def visitif(self, node, parts):
        pass
    def visitfor(self, node, parts):
        pass
    def visitwhile(self, node, parts):
        pass
    def visitcase(self, node, parts):
        pass
    def visituntil(self, node, parts):
        pass
    def visitcommand(self, n, parts):
        pass
    def visitfunction(self, n, name, body, parts):
        pass
    def visitword(self, n, word):
        pass
    def visitassignment(self, n, word):
        pass
    def visitreservedword(self, n, word):
        pass
    def visitparameter(self, n, value):
        pass
    def visittilde(self, n, value):
        pass
    def visitredirect(self, n, input, type, output, heredoc):
        pass
    def visitheredoc(self, n, value):
        pass
    def visitprocesssubstitution(self, n, command):
        pass
    def visitcommandsubstitution(self, n, command):
        pass

# Add indent for each part
# Tree is a list
def _dump(tree, indent='  '):
    def _format(n, level=0):
        if isinstance(n, node):
            d = dict(n.__dict__)
            kind = d.pop('kind')
            if kind == 'list' and level > 0:
                level = level + 1
            fields = []
            v = d.pop('s', None)
            if v:
                fields.append(('s', _format(v, level)))
            for k, v in sorted(d.items()):
                if not v or k == 'parts':
                    continue
                llevel = level
                if isinstance(v, node):
                    llevel += 1
                    fields.append((k, '\n' + (indent * llevel) + _format(v, llevel)))
                else:
                    fields.append((k, _format(v, level)))
            if kind == 'function':
                fields = [f for f in fields if f[0] not in ('name', 'body')]
            v = d.pop('parts', None)
            if v:
                fields.append(('parts', _format(v, level)))
            return ''.join([
                '%sNode' % kind.title(),
                '(',
                ', '.join('%s=%s' % field for field in fields),
                ')'])
        elif isinstance(n, list):
            lines = ['[']
            lines.extend((indent * (level + 1) + _format(x, level + 1) + ','
                         for x in n))
            if len(lines) > 1:
                lines.append(indent * (level) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(n)

    if not isinstance(tree, node):
        raise TypeError('expected node, got %r' % tree.__class__.__name__)
    return _format(tree)

def findfirstkind(parts, kind):
    for i, node in enumerate(parts):
        if node.kind == kind:
            return i
    return -1

class posconverter(nodevisitor):
    def __init__(self, string):
        self.string = string

    def visitnode(self, node):
        assert hasattr(node, 'pos'), 'node %r is missing pos attr' % node
        start, end = node.__dict__.pop('pos')
        node.s = self.string[start:end]

class posshifter(nodevisitor):
    def __init__(self, count, lineno):
        self.count = count
        self.lineno = lineno

    def visitnode(self, node):
        #assert node.pos[1] + base <= endlimit
        node.pos = (node.pos[0] + self.count, node.pos[1] + self.count)
        if hasattr(node, 'lineno'):
            node.lineno = node.lineno + self.lineno
