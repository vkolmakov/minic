from rply import LexerGenerator
from compiler.lexer.tokens import name_with_pattern


class Lexer:
    def __init__(self):
        self.lexer = self.build_lexer()

    def build_lexer(self):
        lg = LexerGenerator()

        for (name, pattern) in name_with_pattern:
            lg.add(name, pattern)

        lg.ignore(r'\s+')

        return lg.build()

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
