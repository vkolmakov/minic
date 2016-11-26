from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.typechecker.typechecker import Typechecker


def create_compiler(with_logger):
    class Compiler:
        def __init__(self):
            self.lexer = Lexer()
            self.parser = Parser()
            self.typechecker = Typechecker()

        @with_logger.log_result('LEXER')
        def lex(self, source):
            return self.lexer.lex(source)

        @with_logger.log_result('PARSER')
        def parse(self, source):
            return self.parser.parse(self.lex(source))

        @with_logger.log_result('TYPECHECKER')
        def typecheck(self, source):
            return self.typechecker.typecheck(self.parse(source))

    compiler = Compiler()
    return compiler
