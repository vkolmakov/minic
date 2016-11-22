from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.token_to_regex = {
            'IF': r'if',
            'ELSE': r'else',

            'LPAREN': r'\(',
            'RPAREN': r'\)',
            'LBRACE': r'\[',
            'RBRACE': r'\]',
            'LCURLY': r'\{',
            'RCURLY': r'\}',

            'SEMI': r';',
            'EQUAL': r'=',

            'EQUAL_EQUAL': r'=',
            'GREATER': r'>',
            'GREATER_EQUAL': r'>=',
            'SMALLER': r'<',
            'SMALLER_EQUAL': r'<=',

            'NUMBER': r'\d+',
            'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',
        }

        self.lexer = self.build_lexer()

    def build_lexer(self):
        lg = LexerGenerator()

        for (name, pattern) in self.token_to_regex.items():
            lg.add(name, pattern)

        lg.ignore(r'\s+')

        return lg.build()

    def token_names(self):
        return self.token_to_regex.keys()

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
