import ply.yacc as yacc
from lex import tokens


def p_error(t):
    print('An error occurred while parsing.')


parser = yacc.yacc(debug=False, write_tables=False)
