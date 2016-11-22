from rply import LexerGenerator


class Lexer:
    def __init__(self):
        lg = LexerGenerator()

        lg.ignore(r'\s+')
        lg.add('IF', r'if')
        lg.add('ELSE', r'else')

        lg.add('LPAREN', r'\(')
        lg.add('RPAREN', r'\)')
        lg.add('LBRACE', r'\[')
        lg.add('RBRACE', r'\]')
        lg.add('LCURLY', r'\{')
        lg.add('RCURLY', r'\}')

        lg.add('SEMI', r';')
        lg.add('EQUAL', r'=')

        lg.add('EQUAL_EQUAL', r'=')
        lg.add('GREATER', r'>')
        lg.add('GREATER_EQUAL', r'>=')
        lg.add('SMALLER', r'<')
        lg.add('SMALLER_EQUAL', r'<=')

        lg.add('NUMBER', r'\d+')
        lg.add('ID', r'[a-zA-Z_][a-zA-Z0-9_]*')

        self.lexer = lg.build()
        self.stream = self.lexer.lex('')  # empty lexer

    def lex(self, source):
        self.stream = self.lexer.lex(source)

    def __next__(self):
        return next(self.stream)

    def __iter__(self):
        while self.stream:
            yield next(self)
