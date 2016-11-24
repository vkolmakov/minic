import unittest
from itertools import zip_longest
from rply import Token

from compiler.lexer.lexer import Lexer


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

    def test_float_numbers(self):
        '''Can lex floating numbers: `x = 55.25 + 44. - 3 + 2.0;`'''
        given = 'x = 55.25 + 44. - 3 + 2.0;'

        expected = iter([
            Token('ID', 'x'),
            Token('EQUAL', '='),
            Token('FLOAT', '55.25'),
            Token('PLUS', '+'),
            Token('FLOAT', '44.'),
            Token('MINUS', '-'),
            Token('INTEGER', '3'),
            Token('PLUS', '+'),
            Token('FLOAT', '2.0'),
            Token('SEMI', ';'),
        ])

        result = lexer.lex(given)

        for (r, e) in zip_longest(result, expected):
            assert r == e


class TestKeywords(unittest.TestCase):
    def test_keywords(self):
        '''Can distinguish between ids and keywords: `float x; int y; if duck else goose` '''
        given = 'float x; int y; if duck else goose'

        expected = iter([
            Token('FLOAT_TYPE', 'float'),
            Token('ID', 'x'),
            Token('SEMI', ';'),

            Token('INT_TYPE', 'int'),
            Token('ID', 'y'),
            Token('SEMI', ';'),

            Token('IF', 'if'),
            Token('ID', 'duck'),
            Token('ELSE', 'else'),
            Token('ID', 'goose'),
        ])

        result = lexer.lex(given)

        for (r, e) in zip_longest(result, expected):
            assert r == e
