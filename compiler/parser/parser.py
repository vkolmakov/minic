from rply import ParserGenerator
import compiler.parser.ast as ast
from compiler.lexer.Lexer import Lexer


pg = ParserGenerator(
    Lexer.token_names(),
    precedence = [
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)


# Statements
@pg.production('main : statements')
def main(s):
    return s[0]


@pg.production('statements : statements statement')
def statements(s):
    return ast.Block(s[0].getastlist() + [s[1]])


@pg.production('statements : statement')
def statements_statement(s):
    return ast.Block([s[0]])


@pg.production('statement : expr SEMI')
def statement_expr(s):
    return ast.Statement(s[0])


@pg.production('statement : variable EQUAL expr SEMI')
def statement_assignment(s):
    return ast.Assignment(s[0], s[2])


# Variables
@pg.production('variable : ID')
def variable(s):
    return ast.ID(s[0].getstr())


# Expressions
@pg.production('expr : LPAREN expr RPAREN')
def expr_parens(p):
    return p[1]


@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
def expr_binop(s):
    return ast.BinOp(s[1].getstr(), s[0], s[2])


@pg.production('expr : INTEGER')
@pg.production('expr : variable')
def expr_leaf(s):
    if isinstance(s[0], ast.AstNode):
        return s[0]
    else:
        return ast.Integer(int(s[0].getstr()))


# Errors
@pg.error
def error_handler(token):
    raise ValueError('Invalid token, %s' % token.gettokentype())

parser = pg.build()
