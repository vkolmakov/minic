import unittest
from itertools import zip_longest
from rply import Token

import compiler.parser.ast as ast
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


    def test_compiler_parse(self):
        '''Can parse a simple program:'''
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

        result = compiler.parse(given)

        expected = ast.Block([
            ast.Declaration(
                'float',
                [ast.ID('duck'), ast.ID('goose'), ast.ArrayRef(ast.ID('birds'), ast.Integer(2))]
            ),
            ast.Declaration('int', [ast.ID('wildcat')]),

            ast.Assignment(ast.ID('duck'), ast.Float(1.0)),
            ast.Assignment(ast.ID('goose'), ast.UnaryOp('-', ast.Integer(1))),

            ast.Assignment(ast.ID('wildcat'), ast.Integer(1)),

            ast.Assignment(ast.ArrayRef(ast.ID('birds'), ast.Integer(0)), ast.ID('duck')),

            ast.IfStatement(
                ast.ID('duck'),
                ast.Block([
                    ast.Assignment(ast.ArrayRef(ast.ID('birds'), ast.Integer(1)), ast.ID('goose'))
                ]),
                ast.Block([
                    ast.Assignment(ast.ArrayRef(ast.ID('birds'), ast.Integer(1)), ast.ID('wildcat'))
                ])
            ),
        ])

        assert result == expected
