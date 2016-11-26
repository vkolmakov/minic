from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.typechecker.typechecker import Typechecker


class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.typechecker = Typechecker()

    def lex(self, source):
        return self.lexer.lex(source)

    def parse(self, source):
        return self.parser.parse(self.lex(source))

    def typecheck(self, source):
        return self.typechecker.typecheck(self.parse(source))
