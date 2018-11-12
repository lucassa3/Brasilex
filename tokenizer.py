from rply import LexerGenerator, ParserGenerator
lg = LexerGenerator()

class SymbolTable():
    def __init__(self):
        self.table = {}

    def get_var(self, varname):
        if varname not in self.table.keys():
            raise ValueError(f"Variable {varname} does not exist!")
        else:
            return self.table[varname]

    def set_var(self, varname, value):     
        self.table[varname] = value

lg.add('NUMBER', r'\d+')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MUL', r'\*')
lg.add('DIV', r'/')
lg.add('OPEN_PAR', r'\(')
lg.add('CLOSE_PAR', r'\)')
lg.add('OPEN_BLOCK', r'\{')
lg.add('CLOSE_BLOCK', r'\}')
lg.add('PRINCIPAL', r'principal')
lg.add('VAZIO', r'vazio')
lg.add('IMPRIME', r'imprime')
lg.add('VARIAVEL', r'var')
lg.add('CMD_END', r';')
lg.add('GE', r'>=')
lg.add('LE', r'<=')
lg.add('EQUAL', r'=')
lg.add('EQUALS', r'==')
lg.add('GREATER', r'>')
lg.add('LESS', r'<')
lg.add('ENQUANTO', r'enquanto')
lg.add('E', r'e')
lg.add('OU', r'ou')
lg.add('SENAO', r'senao')
lg.add('SE', r'se')

lg.add('IDENTIFIER', "[a-zA-Z_][a-zA-Z0-9_]*")
lg.ignore('\s+')

lexer = lg.build()


class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

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

pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['NUMBER', 'OPEN_PAR', 'CLOSE_PAR',
     'PLUS', 'MINUS', 'MUL', 'DIV', 'OPEN_BLOCK', 'CLOSE_BLOCK', 
     'PRINCIPAL', 'VAZIO', 'IMPRIME', 'VARIAVEL', 
     'CMD_END', 'EQUAL', 'IDENTIFIER', 'EQUALS', 'GREATER', 'LESS', 'GE', 'LE', 'E', 'OU', 'SE', 'SENAO', 'ENQUANTO'
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV']),
        ('left', ['AND', 'OR']),
    ]
)



@pg.production('program : VAZIO PRINCIPAL OPEN_BLOCK commands CLOSE_BLOCK') #tem que mudar pra commands depois
def program(p):
    return p[3]

@pg.production('commands : command')
def commands_single(p):
    result = CommandsNode()
    result.set_child(p[0])
    return result


@pg.production('commands : command commands')
def commands(p):
    if type(p[1]) is CommandsNode:
        com = p[1]
    else:
        com = CommmandsNode(p[1])
    
    com.set_child(p[0])
    return com

@pg.production('command : IMPRIME OPEN_PAR expression CLOSE_PAR CMD_END')
def print_com(p):
    return PrintNode(p[2])


@pg.production('command : IDENTIFIER EQUAL expression CMD_END')
def assign_com(p):
    result = AssignerNode(p[0].getstr())
    result.set_child(p[2])
    return result

@pg.production('command : SE OPEN_PAR boolean_expression CLOSE_PAR OPEN_BLOCK commands CLOSE_BLOCK')
def if_com(p):
    result = CondNode()
    result.set_child(p[2])
    result.set_child(p[5])
    return result

@pg.production('command : SE OPEN_PAR boolean_expression CLOSE_PAR OPEN_BLOCK commands CLOSE_BLOCK SENAO OPEN_BLOCK commands CLOSE_BLOCK')
def if_else_com(p):
    result = CondNode()
    result.set_child(p[2])
    result.set_child(p[5])
    result.set_child(p[9])
    return result

@pg.production('command : ENQUANTO OPEN_PAR boolean_expression CLOSE_PAR OPEN_BLOCK commands CLOSE_BLOCK')
def while_com(p):
    result = LoopNode()
    result.set_child(p[2])
    result.set_child(p[5])
    return result


@pg.production('boolean_expression : rel_expr')
def boolean_expr(p):
    return p[0]

@pg.production('boolean_expression : rel_expr OU rel_expr')
@pg.production('boolean_expression : rel_expr E rel_expr')
def boolean_expr_full(p):
    result = BinOp(p[1])
    result.set_child(p[0])
    result.set_child(p[2])

    return result

@pg.production('rel_expr : expression GREATER expression')
@pg.production('rel_expr : expression LESS expression')
@pg.production('rel_expr : expression GE expression')
@pg.production('rel_expr : expression LE expression')
@pg.production('rel_expr : expression EQUALS expression')
def rel_expr(p):
    print("cai aqui")
    result = BinOp(p[1])
    result.set_child(p[0])
    result.set_child(p[2])

    return result

@pg.production('expression : NUMBER')
def expression_number(p):
    return IntVal(int(p[0].getstr()))

@pg.production('expression : IDENTIFIER')
def expression_number(p):
    return IdentifierNode(p[0].getstr())

@pg.production('expression : OPEN_PAR expression CLOSE_PAR')
def expression_par(p):
    return p[1]

@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')

def expression_binop(p):
    result = BinOp(p[1])
    result.set_child(p[0])
    result.set_child(p[2])

    return result

parser = pg.build()

program = """
vazio principal {
    x = 2 * 2*(5+5);
    imprime(x);
    
    se (x > 20 e x < 41) {
        x = x - 1;
        imprime(x);
    }
    senao {
        imprime(1000);
    }
    
    top = 10;

    enquanto (top > 0) {
        top = top - 1;
        imprime(top);
    }


}
"""

for token in lexer.lex(program):
    print(token)

parser.parse(lexer.lex(program)).eval(SymbolTable())
