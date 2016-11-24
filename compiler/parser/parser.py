from rply import ParserGenerator

from compiler.parser.productions import add_productions
from compiler.lexer.tokens import names as token_names


class Parser:
    def __init__(self):
        self.parser = self.build_parser()

    def build_parser(self):
        pg = ParserGenerator(
            token_names,
            precedence = [
                ('left', ['NOT_EQUAL', 'EQUAL_EQUAL', 'GREATER', 'GREATER_EQUAL', 'SMALLER', 'SMALLER_EQUAL']),
                ('left', ['OR', 'AND']),
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV', 'MOD'])
            ]
        )

        return add_productions(pg).build()

    def parse(self, tokens):
        return self.parser.parse(tokens)
