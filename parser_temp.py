from rply import ParserGenerator
from nodes import *


def parse():
    pg=ParserGenerator(
        [
            'NUMBER', 
            'OPEN_PAR', 
            'CLOSE_PAR',
            'PLUS', 
            'MINUS', 
            'MUL', 
            'DIV', 
            'OPEN_BLOCK', 
            'CLOSE_BLOCK',
            'COMMA', 
            'IMPRIME',
            'ESCANEIA',
            'CMD_END', 
            'EQUAL', 
            'IDENTIFIER', 
            'EQUALS', 
            'GREATER', 
            'LESS', 
            'GE', 
            'LE', 
            'E', 
            'OU', 
            'SE', 
            'SENAO',
            'NAO', 
            'ENQUANTO'
        ],

        precedence=[
            ('left', ['PLUS', 'MINUS']),
            ('left', ['MUL', 'DIV']),
            ('left', ['AND', 'OR']),
        ]
    )


    @pg.production('program : commands') 
    def program(p):   
        temp = p[0].children[0]
        p[0].children[0] = FuncCallNode(value='principal')
        p[0].set_child(temp)
        return p[0]


    @pg.production('command : IDENTIFIER OPEN_PAR args CLOSE_PAR OPEN_BLOCK commands CLOSE_BLOCK') 
    def program(p):
        result = FuncDecNode(value=p[0].getstr(), args=p[2][::-1])
        result.set_child(p[5])
        return result

    @pg.production('args : IDENTIFIER')
    def commands_single(p):
        result = [p[0].getstr()]
        return result

    @pg.production('args :')
    def commands_single(p):
        result = []
        return result
    
    @pg.production('args : IDENTIFIER COMMA args') 
    def program(p):
        p[2].append(p[0].getstr())
        return p[2]

    @pg.production('commands : command')
    def commands_single(p):
        result = CommandsNode()
        result.set_child(p[0])
        return result

    @pg.production('commands : command commands')
    def commands(p):
        p[1].set_child(p[0])
        return p[1]

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

    @pg.production('command : IDENTIFIER OPEN_PAR call_args CLOSE_PAR CMD_END')
    def while_com22(p):
        result = FuncCallNode(value=p[0].getstr(), call_args=p[2][::-1])
        return result

    @pg.production('call_args : expression')
    def commands_single(p):
        result = [p[0]]
        return result

    @pg.production('call_args :')
    def commands_single(p):
        result = []
        return result
    
    @pg.production('call_args : expression COMMA call_args') 
    def program(p):
        p[2].append(p[0])
        return p[2]


    @pg.production('boolean_expression : bool_term')
    @pg.production('bool_term : bool_factor')
    @pg.production('bool_factor : rel_expr')
    @pg.production('expression : term')
    @pg.production('term : factor')
    def boolean_expr(p):
        return p[0]

    @pg.production('bool_factor : NAO bool_factor')
    @pg.production('factor : PLUS factor')
    @pg.production('factor : MINUS factor')
    def boolean_expr_fullasdasd(p):
        result = UnOp(p[0])
        result.set_child(p[1])

        return result

    @pg.production('factor : ESCANEIA OPEN_PAR CLOSE_PAR')
    def if_com(p):
        result = ScanNode()
        return result

    @pg.production('boolean_expression : bool_term OU boolean_expression')
    @pg.production('bool_term : bool_factor E bool_term')
    @pg.production('expression : term PLUS expression')
    @pg.production('expression : term MINUS expression')
    @pg.production('term : factor MUL term')
    @pg.production('term : factor DIV term')
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
        result = BinOp(p[1])
        result.set_child(p[0])
        result.set_child(p[2])

        return result

    @pg.production('factor : NUMBER')
    def expression_number(p):
        return IntVal(int(p[0].getstr()))

    @pg.production('factor : IDENTIFIER')
    def expression_number(p):
        return IdentifierNode(p[0].getstr())

    @pg.production('factor : OPEN_PAR expression CLOSE_PAR')
    @pg.production('bool_factor : OPEN_PAR boolean_expression CLOSE_PAR')
    def expression_par(p):
        return p[1]

    return pg.build()