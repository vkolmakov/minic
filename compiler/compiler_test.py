import unittest
from itertools import zip_longest
from rply import Token

from compiler.compiler import Compiler


compiler = Compiler()


class CompilerTest(unittest.TestCase):
    def test_compiler_lex(self):
        '''Can tokenize a simple program:'''
        given = '''
            float duck, goose, birds[2];
            int wildcat;

            duck = 1.0;
            goose = -1;

            wildcat = 1;

            birds[0] = duck;

            if (duck) {
              birds[1] = goose;
            } else {
              birds[1] = wildcat;
            }
        '''

        result = compiler.lex(given)

        expected = [
            Token('FLOAT_TYPE', 'float'), Token('ID', 'duck'), Token('COMMA', ','), Token('ID', 'goose'),
            Token('COMMA', ','), Token('ID', 'birds'), Token('LBRACE', '['), Token('INTEGER', '2'),
            Token('RBRACE', ']'), Token('SEMI', ';'),
            Token('INT_TYPE', 'int'), Token('ID', 'wildcat'), Token('SEMI', ';'),
            Token('ID', 'duck'), Token('EQUAL', '='), Token('FLOAT', '1.0'), Token('SEMI', ';'),
            Token('ID', 'goose'), Token('EQUAL', '='), Token('MINUS', '-'), Token('INTEGER', '1'), Token('SEMI', ';'),
            Token('ID', 'wildcat'), Token('EQUAL', '='), Token('INTEGER', '1'), Token('SEMI', ';'),
            Token('ID', 'birds'), Token('LBRACE', '['), Token('INTEGER', '0'), Token('RBRACE', ']'),
            Token('EQUAL', '='), Token('ID', 'duck'), Token('SEMI', ';'),
            Token('IF', 'if'), Token('LPAREN', '('), Token('ID', 'duck'), Token('RPAREN', ')'), Token('LCURLY', '{'),
            Token('ID', 'birds'), Token('LBRACE', '['), Token('INTEGER', '1'), Token('RBRACE', ']'),
            Token('EQUAL', '='), Token('ID', 'goose'), Token('SEMI', ';'),
            Token('RCURLY', '}'),
            Token('ELSE', 'else'), Token('LCURLY', '{'),
            Token('ID', 'birds'), Token('LBRACE', '['), Token('INTEGER', '1'), Token('RBRACE', ']'),
            Token('EQUAL', '='), Token('ID', 'wildcat'), Token('SEMI', ';'),
            Token('RCURLY', '}')
        ]

        for (r, e) in zip_longest(result, expected):
            assert r == e
