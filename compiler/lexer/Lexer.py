from rply import LexerGenerator


token_to_regex = {
    # 'IF': r'if',
    # 'ELSE': r'else',
    'INT_TYPE': r'int',

    'LPAREN': r'\(',
    'RPAREN': r'\)',
    # 'LBRACE': r'\[',
    # 'RBRACE': r'\]',
    # 'LCURLY': r'\{',
    # 'RCURLY': r'\}',

    'SEMI': r';',
    'COMMA': r',',
    'EQUAL': r'=',

    # 'EQUAL_EQUAL': r'==',
    # 'GREATER': r'>',
    # 'GREATER_EQUAL': r'>=',
    # 'SMALLER': r'<',
    # 'SMALLER_EQUAL': r'<=',

    'INTEGER': r'\d+',
    'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',

    'PLUS': r'\+',
    'MINUS': r'\-',
    'MUL': r'\*',
    'DIV': r'\/',
}


class Lexer:
    def __init__(self):
        self.lexer = self.build_lexer()

    def build_lexer(self):
        lg = LexerGenerator()

        for (name, pattern) in token_to_regex.items():
            lg.add(name, pattern)

        lg.ignore(r'\s+')

        return lg.build()

    @staticmethod
    def token_names():
        return list(token_to_regex.keys())

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
