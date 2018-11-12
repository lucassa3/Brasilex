from st import  SymbolTable
import sys
from lexer import tokenize
from parser_temp import parse


lexer = tokenize()
parser = parse()


with open(sys.argv[1], 'r') as myfile:
    program = myfile.read().replace('\n', '')
    for token in lexer.lex(program):
        print(token)

    parser.parse(lexer.lex(program)).eval(SymbolTable())

