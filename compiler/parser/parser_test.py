import unittest
from rply import Token

from compiler.parser.parser import parser
import compiler.parser.ast as ast


class TestExpr(unittest.TestCase):
    def test_add(self):
        given = iter([
            Token('INTEGER', '1'),
            Token('PLUS', '+'),
            Token('INTEGER', '1'),
            Token('SEMI', ';')
        ])

        expected = ast.Block([
            ast.Statement(ast.BinOp('+', ast.Integer(1), ast.Integer(1)))
        ])

        result = parser.parse(given)

        assert expected == result

    def test_op_order(self):
        given = iter([
            Token('INTEGER', '1'),
            Token('PLUS', '+'),
            Token('INTEGER', '5'),
            Token('MUL', '*'),
            Token('INTEGER', '20'),
            Token('SEMI', ';')
        ])

        expected = ast.Block([
            ast.Statement(
                ast.BinOp(
                    '+',
                    ast.Integer(1),
                    ast.BinOp('*', ast.Integer(5), ast.Integer(20))
                )
            )
        ])

        result = parser.parse(given)

        assert expected == result

    def test_parens(self):
        given = iter([
            Token('LPAREN', '('),
            Token('INTEGER', '1'),
            Token('PLUS', '+'),
            Token('INTEGER', '5'),
            Token('RPAREN', ')'),
            Token('MUL', '*'),
            Token('INTEGER', '20'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Statement(
                ast.BinOp(
                    '*',
                    ast.BinOp('+', ast.Integer(1), ast.Integer(5)),
                    ast.Integer(20)
                )
            )
        ])

        assert result == expected
