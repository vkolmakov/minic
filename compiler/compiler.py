from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser


class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()

    def lex(self, source):
        return self.lexer.lex(source)

    def parse(self, source):
        return self.parser.parse(self.lex(source))
