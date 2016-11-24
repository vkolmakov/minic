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
@pg.production('statements : statements block')
def statements(s):
    return ast.Block(s[0].getastlist() + [s[1]])


@pg.production('block : LCURLY statements RCURLY')
def block_statements(s):
    return s[1]


@pg.production('statements : statement')
def statements_statement(s):
    return ast.Block([s[0]])


@pg.production('statements : block')
def statements_block(s):
    return s[0]


# Statement
@pg.production('statement : expr SEMI')
def statement_expr(s):
    return ast.Statement(s[0])


@pg.production('statement : variable EQUAL expr SEMI')
def statement_assignment(s):
    return ast.Assignment(s[0], s[2])


@pg.production('statement : type variables SEMI')
def statement_declaration(s):
    return ast.Declaration(s[0],
                           [s[1]] if isinstance(s[1], ast.AstNode) else s[1])


@pg.production('statement : if_statement')
def statement_if_statement(s):
    return s[0]


@pg.production('if_statement : IF LPAREN expr RPAREN block')
def if_statement(s):
    return ast.IfStatement(s[2], s[4], ast.Block([]))


@pg.production('if_statement : IF LPAREN expr RPAREN block ELSE block')
def ifelse_statement(s):
    return ast.IfStatement(s[2], s[4], s[6])


# Types
@pg.production('type : INT_TYPE')
def type(s):
    return s[0].getstr()


# Variables
@pg.production('variables : variables COMMA variable')
def variables_sequence(s):
    return ((s[0] if hasattr(s[0], '__iter__') else [s[0]]) +
            [s[2]])


@pg.production('variables : variable')
def variables_single(s):
    return s[0]


@pg.production('variable : variable LBRACE expr RBRACE')
def variable_arrayref(s):
    return ast.ArrayRef(s[0], s[2])


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
