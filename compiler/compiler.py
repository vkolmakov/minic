from compiler.lexer.lexer import Lexer


class Compiler:
    def __init__(self):
        self.lexer = Lexer()

    def lex(self, source):
        return self.lexer.lex(source)
