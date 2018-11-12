class Node():
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def set_child(self, child):
        self.children.append(child)

class IntVal(Node):
    def eval(self, st):
        return self.value

class BinOp(Node):
    def eval(self, st):
        a = self.children[0].eval(st)
        b = self.children[1].eval(st)

        if self.value.gettokentype() == "MINUS":
            return a - b
        elif self.value.gettokentype() == "PLUS":
            return a + b
        elif self.value.gettokentype() == "MUL":
            return a * b
        elif self.value.gettokentype() == "DIV":
            return a // b
        elif self.value.gettokentype() == "GREATER":
            return a > b
        elif self.value.gettokentype() == "LESS":
            return a < b
        elif self.value.gettokentype() == "GE":
            return a >= b
        elif self.value.gettokentype() == "LE":
            return a <= b
        elif self.value.gettokentype() == "EQUALS":
            return a == b
        elif self.value.gettokentype() == "E":
            return a and b
        elif self.value.gettokentype() == "OU":
            return a or b

class CommandsNode(Node):
    def eval(self, st):
        for child in reversed(self.children):
            child.eval(st)

class PrintNode(Node):
    def eval(self, st):
        print(self.value.eval(st))

class AssignerNode(Node):
    def eval(self, st):
        st.set_var(self.value, self.children[0].eval(st))

class IdentifierNode(Node):
    def eval(self, st):
        return st.get_var(self.value)

class CondNode(Node):
    def eval(self, st):
        if self.children[0].eval(st) == True:
            self.children[1].eval(st)
        else:
            if len(self.children) > 2:
                self.children[2].eval(st)

class LoopNode(Node):
    def eval(self, st):
        while self.children[0].eval(st) == True:
            self.children[1].eval(st)