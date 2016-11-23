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

