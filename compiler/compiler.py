from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.typechecker.typechecker import Typechecker

from compiler.utils import Logger


def create_compiler(with_logger=Logger()):
    class Compiler:
        def __init__(self):
            self.lexer = Lexer()
            self.parser = Parser()
            self.typechecker = Typechecker()

        @with_logger.log('LEXER')
        def lex(self, source):
            return self.lexer.lex(source)

        @with_logger.log('PARSER')
        def parse(self, source):
            return self.parser.parse(self.lex(source))

        @with_logger.log('TYPECHECKER')
        def typecheck(self, source):
            return self.typechecker.typecheck(self.parse(source))

    compiler = Compiler()
    return compiler
