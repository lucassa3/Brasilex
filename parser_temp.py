from rply import ParserGenerator
from nodes import *


def parse():
    pg = ParserGenerator(
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
            'PRINCIPAL', 
            'VAZIO', 
            'IMPRIME', 
            'VARIAVEL', 
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
            'ENQUANTO'
        ],

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

    return pg.build()