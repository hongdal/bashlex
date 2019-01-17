from bashlex import ast, errors
import re

def gatherheredocuments(tokenizer):
    # if we're at the end of the input and we're not strict, allow skipping
    # reading the heredoc
    while tokenizer.redirstack:
        if tokenizer._peekc() is None and not tokenizer._strictmode:
            tokenizer._shell_input_line_index += 1
            return

        redirnode, killleading = tokenizer.redirstack.pop(0)
        makeheredoc(tokenizer, redirnode, 0, killleading)

def makeheredoc(tokenizer, redirnode, lineno, killleading):
    redirword = remove_escape(string_quote_removal(redirnode.output.word))
    #redirword = redirnode.output.word
    document = []

    startpos = tokenizer._shell_input_line_index

    #fullline = self.tok.readline(bool(redirword.output.flags & flags.word.QUOTED))
    fullline = tokenizer.readline(False)
    while fullline:
        if killleading:
            while fullline[0] == '\t':
                fullline = fullline[1:]

        if not fullline:
            continue

        if fullline[:-1] == redirword and fullline[len(redirword)] == '\n':
            document.append(fullline[:-1])
            # document_done
            break

        document.append(fullline)
        #fullline = self.readline(bool(redirnode.flags & flags.word.QUOTED))
        fullline = tokenizer.readline(False)

    if not fullline:
        raise errors.ParsingError("here-document at line %d delimited by end-of-file (wanted %r)" % (lineno, redirword), tokenizer._shell_input_line, tokenizer._shell_input_line_index)

    document = ''.join(document)
    endpos = tokenizer._shell_input_line_index - 1

    assert hasattr(redirnode, 'heredoc')
    num_of_lines = document.count('\n') + 1
    redirnode.heredoc = ast.node(kind='heredoc', value=document,
                                 pos=(startpos, endpos), lineno=num_of_lines)

    # if the heredoc immediately follows this node, fix its end pos
    if redirnode.pos[1] + 1 == startpos:
        redirnode.pos = (redirnode.pos[0], endpos)

    return document

def string_quote_removal(s):
    ''' removes potential leading and ending 's or "s (only if they match)
        for variable expansion disabling in heredoc '''
    return re.sub(r'^[\'"]|[\'"]$', '', s)

def remove_escape(s):
    '''escaped delimiter in heredoc also disables variable expansion'''
    if s[0] == "\\":
        return s[1:]
    return s
