import unittest
from itertools import zip_longest
from rply import Token

from compiler.lexer.Lexer import Lexer


lexer = Lexer()


class TestSimpleStrings(unittest.TestCase):
    def test_arithmetic(self):
        '''Can lex a simple arithmetic expression: `20 + 100 * 30 == 3020;` '''
        given = '20 + 100 * 30 == 3020;'

        expected = iter([
            Token('INTEGER', '20'),
            Token('PLUS', '+'),
            Token('INTEGER', '100'),
            Token('MUL', '*'),
            Token('INTEGER', '30'),
            Token('EQUAL_EQUAL', '=='),
            Token('INTEGER', '3020'),
            Token('SEMI', ';'),
        ])

        result = lexer.lex(given)

        for (r, e) in zip_longest(result, expected):
            assert r == e

    def test_arithmetic_with_ids(self):
        '''Can lex a simple expression: `x = 55 + y;`'''
        given = 'x = 55 + y;'

        expected = iter([
            Token('ID', 'x'),
            Token('EQUAL', '='),
            Token('INTEGER', '55'),
            Token('PLUS', '+'),
            Token('ID', 'y'),
            Token('SEMI', ';'),
        ])

        result = lexer.lex(given)

        for (r, e) in zip_longest(result, expected):
            assert r == e
