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
                ('left', ['EQUAL_EQUAL', 'GREATER', 'GREATER_EQUAL', 'SMALLER', 'SMALLER_EQUAL']),
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV'])
            ]
        )

        pg1 = add_productions(pg)

        return pg1.build()

    def parse(self, tokens):
        return self.parser.parse(tokens)
