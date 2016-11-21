import ply.yacc as yacc
from lexer.lex import tokens

import parser.ast.primitives

def p_statement_list(p):
    r'''statement_list : statement statement_list SEMI
                       | statement SEMI'''
    print('statement_list', p)

def p_statement(p):
    r'''statement : composite_statement
                  | expression
                  | declarations_sequence
                  | IF LPAREN relational_expression RPAREN statement
                  | IF LPAREN relational_expression RPAREN statement ELSE statement
                  | SEMI'''
    print('statement', p)


def p_composite_statement(p):
    r'''composite_statement : LCURLY statement_list RCURLY
                            | LCURLY RCURLY'''
    print('composite_statement', p)


# Declarations
def p_declarations_sequence(p):
    r'''declarations_sequence : type variables_sequence
                              | type variable_name'''
    print('from sequence', p[1], p[2])


def p_variables_sequence(p):
    r'''variables_sequence : variable_name COMMA variables_sequence
                           | variable_name'''
    print('variables', p[1])

def p_type(p):
    r'''type : INT
             | FLOAT'''

    kwd_to_type = {
        'int': ast.types.IntType,
        'float': ast.types.FloatType,
    }

    p[0] = kwd_to_type.get(p[1], ast.types.UnknownType)()


# Expressions
def p_expressions_sequence(p):
    r'''expressions_sequence : expressions_sequence COMMA expression
                             | expression'''


def p_stop_statement(p):
    r'''stop_statement : SEMI'''
    print('stop_statement', p)


def p_expression(p):
    r'''expression : rhs
                   | modify_expression'''
    print('expression', p)


def p_modify_expression(p):
    r'''modify_expression : variable_name EQUALS rhs
                          | ID EQUALS rhs'''  # ???
    print('modify_expression', p)


def p_rhs(p):
    r'''rhs : binary_expression
            | unary_expression'''
    print('rhs', p)


def p_unary_expression(p):
    r'''unary_expression : simple_expression
                         | unary_operator value'''
    print('unary_expression', p)


def p_binary_expression(p):
    r'''binary_expression : value binary_operator value'''


def p_unary_operator(p):
    r'''unary_operator : PLUS
                       | MINUS'''


def p_binary_operator(p):
    r'''binary_operator : relational_operator
                        | MINUS
                        | PLUS'''
                        # TODO: Add more ops


def p_relational_operator(p):
    r'''relational_operator : LT
                            | GT'''
                            # TODO: Add more ops


def p_relational_expression(p):
    r'''relational_expression : value
                               | value relational_operator value'''


def p_simple_expression(p):
    r'''simple_expression : variable_name
                          | INT_VAL
                          | FLOAT_VAL'''
    print('simple_expression', p)


def p_value(p):
    r'''value : ID
              | INT_VAL
              | FLOAT_VAL'''
    print('value', p)


def p_variable_name(p):
    r'''variable_name : ID LBRACKET value RBRACKET
                      | ID'''
    if len(p) == 2:
        p[0] = ast.primitives.ID(p[1])
    else:
        pass # TODO: Handle arrayref

def p_array_reference(p):
    r'''array_reference : '''


def p_error(t):
    print('An error occurred while parsing.')


parser = yacc.yacc(debug=False, write_tables=False)
