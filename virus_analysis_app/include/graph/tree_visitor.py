
'''
    The key idea is to parse the .out file line by line. 
    Then we get a hierarchical structure like this: 

    IfNode(
        ReservedwordNode('if')
        ListNode(
            CommandNode('[...]')
            OperatorNode(';')
        )
        ReservedwordNode('then')
        ListNode(
            CommandNode('...')
            OperatorNode(';)
            CommandNode('...')
            OperatorNode('\n')
        )
        ReservedwordNode('elif')
        ListNode(
            CommandNode('...')
            OperatorNode('\n')
            CommandNode('...')
            OperatorNode('\n')
        )
        ReservedwordNode('then)
        ListNode(
            CommandNode('...')
            OperatorNode('\n')
            CommandNode('...')
            OperatorNode('\n')
        )
        ReservedwordNode('else')
        ListNode(
            CommandNode('...')
            OperatorNode('\n')
            CommandNode('...')
            OpeartorNode(';')
        )
        ReservedwordNode('fi')
    )

    To be simple, lets denote it as follows. 

    IfNode
        ReservedwordNode(if)
        ListNode(condition1)
            CommandNode(1)
            CommandNode(2)
        ReservedwordNode(then)
        ListNode(body1)
            CommandNode(3)
            CommandNode(4)
        ReservedwordNode(elif)
        ListNode(condition2)
            CommandNode(5)
            CommandNode(6)
        ReservedwordNode(then)
        ListNode(body2)
            CommandNode(7)
            CommandNode(8)
        ReservedwordNode(else)
        ListNode(body3)
            CommandNode(9)
            CommandNode(10)
        ReservedwordNode(fi)


    Then let's consider IfNode as a blackbox, we get this.


    ListNode
        CommandNode(s)
        CompoundNode
            IfNode
        CommandNode(s)


    We want to make the follwoing connections 
        CommandNode(s) -> CommandNode(1)
        CommandNode(1) -> CommandNode(2)
        CommandNode(2) -> CommandNode(3)
        CommandNode(2) -> CommandNode(5)
        CommandNode(2) -> CommandNode(9)
        CommandNode(2) -> CommandNode(e)
        CommandNode(3) -> CommandNode(4)
        CommandNode(4) -> CommandNode(e)
        CommandNode(5) -> CommandNode(6)
        CommandNode(6) -> CommandNode(7)
        CommandNode(6) -> CommandNode(9)
        CommandNode(6) -> CommandNode(e)
        CommandNode(7) -> CommandNode(8)
        CommandNode(8) -> CommandNode(4)
        CommandNode(9) -> CommandNode(10)
        CommandNode(10) -> CommandNode(e)

    Lets group the connections as follows. 

    (1): What is the first command in IfNode?
        CommandNode(s) -> CommandNode(1)

    (2): What are the connections within an IfNode?
        CommandNode(2) -> CommandNode(3)
        CommandNode(2) -> CommandNode(5)
        CommandNode(2) -> CommandNode(9)
        CommandNode(6) -> CommandNode(7)
        CommandNode(6) -> CommandNode(9) 
        ... 

    (3): How do the command get merged?
        CommandNode(2) -> CommandNode(e)
        CommandNode(4) -> CommandNode(e)
        CommandNode(6) -> CommandNode(e)
        CommandNode(10) -> CommandNode(e)

    Next, let's discuss them one by one. 

    (1): The command immediate after ReservedwordNode('if') is the 
    first command of IfNode. 

    (2): For commands within the same IfNode, the rules are as follows.
    
    1) If a node is in the condition, then its precursors must be the following. 
        + Condition lists before this condition. 

    2) If a node is in the body, then its precursors must be one of the following. 
        + Last commandNode in this body
        + Condition lists before this body

    (3): The last command (let's think nested IfNode as a single command
    within another IfNode) of an IfNode is the union of the last commands
    in each branch body. 
    Then how can we define 'the last command of a branch body'? 
    It is defined as the command immediately before the keywords
    'else', 'elif', and 'fi'.
    If this command is an IfNode, then recursively define it. 
    If this command is a while-do command, it's the union of last command 
    of while condition and its body. 

'''  
from include.scriptdata import ScriptData

NON_COMMAND = ""
BINARY_COMMAND = "BINARY_COMMAND"


class TreeVisitor:
    def __init__(self, tree):
        self.tree = tree
        self.current_path_to_root = []
        self.level = -1
        self.basic_commands = []
        self.cfg = {}
        self.command_detector = ScriptData() 
        self.downloaded_set = set([])
        self.tag_set = set([])
        self.bad_graph = False


    def make_cfg(self):
        self.recursive_visit(self.tree.root)


    '''
        Check whether WordNode and AssignmentNode is expandable or not. 
    ''' 
    def is_expandable(self, node):
        for c in node.children:
            if c.data.kind == "CommandsubstitutionNode":
                return True 
        return False

    '''
        node    : the "Root" node
    '''
    def visit_root_node(self, node):
        is_first_command = True 
        last_command_child = None 
        node.data.precursors = set([])
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may skip
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    # skip if it's not expandable. 
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)
        if last_command_child == None:
            print("Node:%s does not have command children\n" % node.data.kind)
            exit(1)


    def visit_command_node(self, node):
        is_first_command = True
        last_command_child = None
        # If it's a basic command 
        if self.is_basic_command(node):
            # check whether it's "continue"
            if -1 != node.children[0].data.label.find("continue"):
                # 4) compute the continues of the node itself
                node.data.continues.add(node)
                # 5) compute the tails of the node itself, set it to empty.
                node.data.tails = set([])
                return
        # Otherwise it's not a basic command, let's expand it. 
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 5) compute the continues of the node itself
                # It's impossible for a CommandNode has a child that contains "continue"
                # node.data.continues = node.data.continues.union(last_command_child.data.continues)

        # 4) compute the tails of the node itself 
        if last_command_child == None:
            # If all its children are not expandable then use its own as its tail. 
            node.data.tails.add(node)
        else:
            node.data.tails = last_command_child.data.tails

    def visit_list_compound_node(self, node):
        is_first_command = True
        last_command_child = None
        # To handle "||" and "&&" operators
        local_tails = []
        local_tails_terminating = False
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # Handle "||" and "&&" operators
                if node.children[i].data.kind == "OperatorNode":
                    if None == last_command_child:
                        print("Syntax issue: %s operator at the beginning." % node.children[i].data.label)
                        exit(1)
                    if node.children[i].data.label == r"||" or \
                       node.children[i].data.label == r"&&":
                        local_tails.append(last_command_child.data.tails)
                        local_tails_terminating = False
                    else:
                        local_tails_terminating = True
                    continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    # Handle "||" and "&&" operators
                    if True == local_tails_terminating and len(local_tails) > 0:
                        for local_tail in local_tails:
                            node.children[i].data.precursors = node.children[i].data.precursors.union(local_tail)
                        local_tails_terminating = False
                        local_tails = []

                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)
        if last_command_child == None:
            print("Node:%s does not have command children\n" % node.kind)
            exit(1)
        

    def visit_word_assignment_node(self, node):
        is_first_command = True
        last_command_child = None
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            # Only when it's substitution, expand it. 
            if node.children[i].data.kind == "CommandsubstitutionNode":
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)

    '''
        if condition; then 
            command
        elif condition; then
            command
        else
            command
        fi
    '''
    def visit_if_node(self, node):
        # Seperate conditions and bodies
        conditions = []
        bodies = [] 
        for i in range(len(node.children)):
            if node.children[i].data.kind == "ReservedwordNode":
                if (node.children[i].data.label == "if" or node.children[i].data.label == "elif"):
                    conditions.append(node.children[i+1])
                if (node.children[i].data.label == "then" or node.children[i].data.label == "else"):
                    bodies.append(node.children[i+1])
        if len(conditions) != len(bodies)-1 and len(conditions) != len(bodies):
            print("If-else condition and body mismatch\n")
            exit(1)

        self.tag_set.add("if")

        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(conditions)):
            # 1) compute the precursors of all the conditions
            if 0 == i:
                conditions[i].data.precursors = node.data.precursors
            else:
                conditions[i].data.precursors = conditions[i-1].data.tails
            # 2) compute tails of all conditions
            # 3) compute the continues of all conditions
            self.recursive_visit(conditions[i])

        for i in range(len(conditions)):
            # 1) compute the precursors of all bodies
            bodies[i].data.precursors = conditions[i].data.tails 
            # 2) compute tails of all bodies
            # 3) compute the continues of all bodies
            self.recursive_visit(bodies[i])
            # 5) compute the continues of the node itself
            node.data.continues = node.data.continues.union(bodies[i].data.continues)

        # One more body, caused by "else"
        if len(bodies) > len(conditions):
            # 1) compute the precursors of last body 
            bodies[-1].data.precursors = conditions[-1].data.tails
            # 2) compute tails of all last body
            # 3) compute the continues of last body
            self.recursive_visit(bodies[-1])
            # 5) compute the continues of the node itself
            node.data.continues = node.data.continues.union(bodies[-1].data.continues)

        # 4) compute the tails of the IfNode, 
        # using all bodies and the last condition. 
        for i in range(len(bodies)):
            node.data.tails = node.data.tails.union(bodies[i].data.tails)
        node.data.tails = node.data.tails.union(conditions[-1].data.tails)


    def visit_commandsubstitution_node(self, node):
        is_first_command = True
        last_command_child = None
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)
                    
        if last_command_child == None:
            print("Node:%s does not have command children\n" % kind)
            exit(1)

    def visit_pipeline_node(self, node):
        is_first_command = True
        last_command_child = None
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 4) compute the tails of the node itself 
                node.data.tails = last_command_child.data.tails
                # 5) compute the continues of the node itself
                node.data.continues = node.data.continues.union(last_command_child.data.continues)

        if last_command_child == None:
            print("Node:%s does not have command children\n" % node.kind)
            exit(1)

    '''
        For word in word; do 
            command
        done
    '''
    def visit_for_node(self, node):
        is_first_command = True
        last_command_child = None
        first_body = None
        continues_from_children = set([])
        node.data.continues = set([])
        self.tag_set.add("for")
        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        for i in range(len(node.children)):
            # It's a command node
            if node.children[i].data.kind != "ReservedwordNode" and \
                node.children[i].data.kind != "ParameterNode" and \
                node.children[i].data.kind != "OperatorNode" and \
                node.children[i].data.kind != "RedirectNode" and \
                node.children[i].data.kind != "PipeNode": 
                # If it's WordNode or AssignmentNode, may continue. 
                if node.children[i].data.kind == "WordNode" or \
                    node.children[i].data.kind == "AssignmentNode":
                    if not self.is_expandable(node.children[i]):
                        continue
                # 1) compute the precursors of all the children 
                if True == is_first_command:
                    is_first_command = False
                    node.children[i].data.precursors = node.data.precursors
                else:
                    node.children[i].data.precursors = last_command_child.data.tails
                    node.children[i].data.pre = last_command_child
                # 2) compute tails of all the children
                # 3) compute the continues of all the children 
                self.recursive_visit(node.children[i])
                last_command_child = node.children[i]
                # 5) compute the continues of the node itself
                continues_from_children = continues_from_children.union(last_command_child.data.continues)
            # set the first command of the body
            if node.children[i].data.kind == "ReservedwordNode" and \
                node.children[i].data.label == "do":
                first_body = node.children[i+1]

        # update precursors for the first command of the body, 
        # 1) adding tails of the body as the precursors of the first command of the body 
        # 2) adding continues of its children as the precursors of the first command of the body
        # And update all its children
        first_body.data.precursors = first_body.data.precursors.union(last_command_child.data.tails)
        first_body.data.precursors = first_body.data.precursors.union(continues_from_children)
        self.recursive_visit(first_body)

        # 4) compute the tails of the node itself 
        if last_command_child == None:
            print("Node:%s does not have command children\n" % node.kind)
            exit(1)
        else:
            node.data.tails = last_command_child.data.tails.union(continues_from_children)


    '''
        while command; do 
            command 
        done
    '''
    def visit_while_node(self, node):
        # Match the while node pattern
        # while + condition + do + body + done
        if len(node.children) != 5:
            print("Bad WhileNode: lenght=%d\n" % len(node.children))
            exit(1)
        elif node.children[0].data.kind != "ReservedwordNode" or \
                node.children[2].data.kind != "ReservedwordNode":
            print("Bad WhileNode: lenght=%d\n" % len(node.children))
            exit(1) 

        self.tag_set.add("while")

        # 1) compute the precursors of all the children 
        # 2) compute tails of all the children
        # 3) compute the continues of all the children 
        # 4) compute the tails of the node itself 
        # 5) compute the continues of the node itself
        # match the while node condition and body. 
        condition_command_child = node.children[1]
        body_command_child = node.children[3]
        # 1) compute the precursors of the condition
        condition_command_child.data.precursors = node.data.precursors 
        # 2) compute tails of all the condition
        self.recursive_visit(condition_command_child)
        # 1) compute the precursors of the body
        body_command_child.data.precursors = condition_command_child.data.tails
        # 2) compute tails of all the body
        self.recursive_visit(body_command_child)
        # update precursors for condition, 
        # 1) adding tails of body to the condition
        # 2) adding continues in the body to the condition
        condition_command_child.data.precursors = condition_command_child.data.precursors.union(body_command_child.data.tails)
        condition_command_child.data.precursors = condition_command_child.data.precursors.union(body_command_child.data.continues)
        # update all children of condition nodes. 
        # Update precursors of all the children in the condition. 
        self.recursive_visit(condition_command_child)

        # 4) compute the tails of the node itself 
        node.data.tails = condition_command_child.data.tails
        # 5) compute the continues of the node itself
        node.data.continues = set([])

    """
        Set tails of node and 
        Set precursors and tails of its children
    """
    def recursive_visit(self, node):
        kind = node.data.kind
        if "ReservedwordNode" == kind or "ParameterNode" == kind or \
            "OperatorNode" == kind or "RedirectNode" == kind or \
            "PipeNode" == kind:
            node.data.tails = None
            return
        if "Root" == kind:
            self.visit_root_node(node)
        #
        #   Todo: handle "||" and "&&" operation
        #
        elif "ListNode" == kind or "CompoundNode" == kind:
            self.visit_list_compound_node(node)
        elif "WordNode" == kind or "AssignmentNode" == kind:
            self.visit_word_assignment_node(node)
        elif "IfNode" == kind:
            self.visit_if_node(node)
        elif "WhileNode" == kind:
            self.visit_while_node(node)
        elif "ForNode" == kind:
            self.visit_for_node(node)
        elif "CommandNode" == kind:
            self.visit_command_node(node)
        elif "CommandsubstitutionNode" == kind:
            self.visit_commandsubstitution_node(node)
        elif "PipelineNode" == kind:
            self.visit_pipeline_node(node)
        else:
            print("Unknown kind:%s" % kind)
            self.bad_graph = True
            if "FunctionNode" == kind:
                self.tag_set.add("function")
            elif "CaseNode" == kind:
                self.tag_set.add("case")


    def dump_tree(self):
        self.level = -1
        self.recursive_dump_node(self.tree.root)

    def recursive_dump_node(self, node):
        self.level +=  1
        # dump itself. 
        #indent = "  " * int(node.data.level+1)
        indent = "  " * int(self.level)
        content = node.data.kind + "(" + node.data.label + ")"
        print(indent + content)
        for child in node.children:
            self.recursive_dump_node(child)
        self.level -= 1



    def is_basic_command(self, node):
        for child in node.children:
            if "WordNode" == child.data.kind or "AssignmentNode" == child.data.kind:
                if self.is_expandable(child):
                    return False
            elif "ListNode" == child.data.kind or "CompoundNode" == child.data.kind or \
                "IfNode" == child.data.kind or "WhileNode" == child.data.kind or \
                "ForNode" == child.data.kind or "CommandNode" == child.data.kind or \
                "CommandsubstitutionNode" == child.data.kind or "PipelineNode" == child.data.kind:
                return False
            else:
                continue
        return True


    '''
        node must be a basic command, i.e., not expandable any more
    '''
    def label_basic_command(self, node):
        command = ''
        for child in node.children:
            command += " " + child.data.label
        command = command.replace(r'"', r'\"')
        command = command.replace(r'[', r'\[')
        command = command.replace(r']', r'\]')
        # handle unknow commands
        namedic = self.command_detector.inquiryCommandInfo(command)
        if namedic["category"] == "binaryfile":
            if namedic["name"] in self.downloaded_set:
                command = BINARY_COMMAND
        elif namedic["category"] == "network" and namedic["downloaded"] == True:
            self.downloaded_set.add(namedic["filename"])            
        node.data.label = command


    def build_basic_commands(self, node):
        # determine whether it's a basic command. 
        if node.data.kind == "CommandNode":
            # Add a new record to the hash table if it's a basic command. 
            if self.is_basic_command(node):
                self.basic_commands.append(node)
                # update the label of node - This must be the basic command
                self.label_basic_command(node)
                return
        for child in node.children:
            self.build_basic_commands(child)
                

    def build_cfg(self):
        self.basic_commands = []
        self.build_basic_commands(self.tree.root)
        self.cfg = {}
        # traverse the basic command list
        for basic_command in self.basic_commands:
            for precursor in basic_command.data.precursors:
                if precursor in self.cfg:
                    self.cfg[precursor].append(basic_command)
                else:
                    self.cfg[precursor] = [basic_command]


    def print_cfg(self):
        print("digraph {")
        # Print labels for all nodes. 
        for node in self.basic_commands:
            labeling_node = str(node.uid) + ' [label="' + node.data.label + '"];'
            print(labeling_node)
        # Print all the connections.
        for key in self.cfg.keys():
            #labeling_node = str(key.uid) + ' [label="' + key.data.label + '"];'
            #print(labeling_node)
            for node in self.cfg[key]:
                connection = str(key.uid) + ' -> ' + str(node.uid) + ';'
                print(connection)
        print("}")



