import compiler.parser.ast as ast
from compiler.utils import is_iterable


def statements_productions(pg):
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

    return pg


def statement_productions(pg):
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

    return pg


def type_productions(pg):
    # Types
    @pg.production('type : INT_TYPE')
    @pg.production('type : FLOAT_TYPE')
    def type(s):
        return s[0].getstr()

    return pg


def variables_productions(pg):
    # Variables
    @pg.production('variables : variables COMMA variable')
    def variables_sequence(s):
        return ((s[0] if is_iterable(s[0]) else [s[0]]) +
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

    return pg


def expressions_productions(pg):
    # Expressions
    @pg.production('expr : LPAREN expr RPAREN')
    def expr_parens(s):
        return s[1]

    @pg.production('expr : MINUS expr')
    @pg.production('expr : BANG expr')
    def expr_unaryop(s):
        return ast.UnaryOp(s[0].getstr(), s[1])

    @pg.production('expr : expr PLUS expr')
    @pg.production('expr : expr MINUS expr')
    @pg.production('expr : expr MUL expr')
    @pg.production('expr : expr DIV expr')
    @pg.production('expr : expr MOD expr')
    @pg.production('expr : expr OR expr')
    @pg.production('expr : expr AND expr')
    @pg.production('expr : expr EQUAL_EQUAL expr')
    @pg.production('expr : expr NOT_EQUAL expr')
    @pg.production('expr : expr GREATER expr')
    @pg.production('expr : expr GREATER_EQUAL expr')
    @pg.production('expr : expr SMALLER expr')
    @pg.production('expr : expr SMALLER_EQUAL expr')
    def expr_binop(s):
        return ast.BinOp(s[1].getstr(), s[0], s[2])

    @pg.production('expr : INTEGER')
    @pg.production('expr : FLOAT')
    @pg.production('expr : variable')
    def expr_leaf(s):
        if isinstance(s[0], ast.AstNode):
            return s[0]
        else:
            handlers = {
                'INTEGER': lambda t: ast.Integer(int(t.getstr())),
                'FLOAT': lambda t: ast.Float(float(t.getstr())),
            }

            default_handler = lambda t: t  # noqa

            return handlers.get(s[0].gettokentype(), default_handler)(s[0])

    return pg


def error_handler(pg):
    # Errors
    @pg.error
    def error_handler(token):
        raise ValueError('Invalid token, %s' % token.gettokentype())

    return pg


def add_productions(pg):
    production_groups = [
        statements_productions,
        statement_productions,
        type_productions,
        variables_productions,
        expressions_productions,
        error_handler
    ]

    for apply_production_group in production_groups:
        pg = apply_production_group(pg)

    return pg
