from rply import LexerGenerator


name_with_pattern = [
    ('IF', r'if'),
    ('ELSE', r'else'),
    ('INT_TYPE', r'int'),

    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\['),
    ('RBRACE', r'\]'),
    ('LCURLY', r'\{'),
    ('RCURLY', r'\}'),

    ('EQUAL_EQUAL', r'=='),
    ('GREATER', r'>'),
    ('GREATER_EQUAL', r'>='),
    ('SMALLER', r'<'),
    ('SMALLER_EQUAL', r'<='),

    ('INTEGER', r'\d+'),
    # ('FLOAT', r'\d+?\.\d+'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),

    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MUL', r'\*'),
    ('DIV', r'\/'),

    ('SEMI', r';'),
    ('COMMA', r','),
    ('EQUAL', r'='),
]


class Lexer:
    def __init__(self):
        self.lexer = self.build_lexer()

    def build_lexer(self):
        lg = LexerGenerator()

        for (name, pattern) in name_with_pattern:
            lg.add(name, pattern)

        lg.ignore(r'\s+')

        return lg.build()

    @staticmethod
    def token_names():
        return [name for (name, _) in name_with_pattern]

    def lex(self, source):
        stream = self.lexer.lex(source)
        return TokenStream(stream)


class TokenStream:
    def __init__(self, stream):
        self.stream = stream

    def __next__(self):
        return next(self.stream)

    def __iter__(self):
        while self.stream:
            yield next(self)
