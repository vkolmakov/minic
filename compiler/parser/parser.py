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


@pg.production('expr : INTEGER')
def expr_number(s):
    return ast.Integer(int(s[0].getstr()))


@pg.production('expression : LPAREN expression RPAREN')
def expr_parens(p):
    return p[1]


@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
def expr_binop(s):
    return ast.BinOp(s[1].getstr(), s[0], s[2])


parser = pg.build()
