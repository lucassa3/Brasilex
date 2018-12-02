from st import SymbolTable

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


class UnOp(Node):
    def eval(self, st):
        a = self.children[0].eval(st)

        if self.value.gettokentype() == "MINUS":
            return -a
        elif self.value.gettokentype() == "PLUS":
            return +a
        elif self.value.gettokentype() == "NAO":
            return not a

class FuncDecNode(Node):
    def __init__(self, value, args):
        super(self.__class__, self).__init__(value)
        self.args = args

    def eval(self, st):
        st.set_var(self.value, self)


class FuncCallNode(Node):
    def __init__(self, value, call_args = []):
        super(self.__class__, self).__init__(value)
        self.call_args = call_args
    
    def eval(self, st):
        func = st.get_var(self.value)
        if len(func.args) == len(self.call_args):
            if self.call_args:
                for arg, c_arg in zip(func.args, self.call_args):
                    func.children[0].local_st.set_var(arg, c_arg.eval(st))
        else:
            raise ValueError(f"argument number passed doesnt matched! Received {len(self.call_args)} args but function needs {len(func.args)}!")

        func.children[0].eval(st)

        # if func.vartype != "void":
        #     return func.children[0].local_st.get_var("return")

class CommandsNode(Node):
    def __init__(self, value=None):
        super(self.__class__, self).__init__(value)
        self.local_st = SymbolTable()

    def eval(self, st):
        self.local_st.father = st
        for child in reversed(self.children):
            child.eval(self.local_st)

class NullNode(Node):
    def eval(self, st):
        print("nulo")

class PrintNode(Node):
    def eval(self, st):
        print(self.value.eval(st))

class ScanNode(Node):
    def eval(self, st):
        self.value = input("scan: ")
        return int(self.value)

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