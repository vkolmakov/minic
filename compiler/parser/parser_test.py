import unittest
from rply import Token

from compiler.parser.parser import parser
import compiler.parser.ast as ast


class TestExpr(unittest.TestCase):
    def test_add(self):
        '''Can parse a simple addition: `1 + 1;`'''
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
        '''Enforces the right op. precedence: `1 + 5 * 20;`'''
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
        '''Honors parenthesis: `(1 + 5) * 20;`'''
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


class TestAssignment(unittest.TestCase):
    def test_simple_assignment(self):
        '''Can parse a simple assignment: `x = 5;`'''
        given = iter([
            Token('ID', 'x'),
            Token('EQUAL', '='),
            Token('INTEGER', '5'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Assignment(
                ast.ID('x'),
                ast.Integer(5)
            )
        ])

        assert result == expected

    def test_expr_assignment(self):
        '''Can parse assignment to expression: `duck = (5 + 10) * 20;`'''
        given = iter([
            Token('ID', 'duck'),
            Token('EQUAL', '='),
            Token('LPAREN', '('),
            Token('INTEGER', '5'),
            Token('PLUS', '+'),
            Token('INTEGER', '10'),
            Token('RPAREN', ')'),
            Token('MUL', '*'),
            Token('INTEGER', '20'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Assignment(
                ast.ID('duck'),
                ast.BinOp(
                    '*',
                    ast.BinOp('+', ast.Integer(5), ast.Integer(10)),
                    ast.Integer(20)
                )
            )
        ])

        assert result == expected

    def test_assignment_to_id(self):
        '''Can parse assignment to another id: `x = y`'''
        given = iter([
            Token('ID', 'x'),
            Token('EQUAL', '='),
            Token('ID', 'y'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Assignment(
                ast.ID('x'),
                ast.ID('y')
            )
        ])

        assert result == expected

    def test_expr_assignment_with_ids(self):
        '''Can parse assignment to expression with ids:
           `duck = (goose + 10) * duck;`'''
        given = iter([
            Token('ID', 'duck'),
            Token('EQUAL', '='),
            Token('LPAREN', '('),
            Token('ID', 'goose'),
            Token('PLUS', '+'),
            Token('INTEGER', '10'),
            Token('RPAREN', ')'),
            Token('MUL', '*'),
            Token('ID', 'duck'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Assignment(
                ast.ID('duck'),
                ast.BinOp(
                    '*',
                    ast.BinOp('+', ast.ID('goose'), ast.Integer(10)),
                    ast.ID('duck')
                )
            )
        ])

        assert result == expected

    def test_assignment_to_id(self):
        '''Can parse multiple assignments:
           `x = 5;
            y = 10 * z;
            sum_times_five = (x + y) * 5;`'''
        given = iter([
            Token('ID', 'x'),
            Token('EQUAL', '='),
            Token('INTEGER', '5'),
            Token('SEMI', ';'),
            Token('ID', 'y'),
            Token('EQUAL', '='),
            Token('INTEGER', '10'),
            Token('MUL', '*'),
            Token('ID', 'z'),
            Token('SEMI', ';'),
            Token('ID', 'sum_times_five'),
            Token('EQUAL', '='),
            Token('LPAREN', '('),
            Token('ID', 'x'),
            Token('PLUS', '+'),
            Token('ID', 'y'),
            Token('RPAREN', ')'),
            Token('MUL', '*'),
            Token('INTEGER', '5'),
            Token('SEMI', ';'),
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Assignment(
                ast.ID('x'),
                ast.Integer(5)
            ),
            ast.Assignment(
                ast.ID('y'),
                ast.BinOp('*', ast.Integer(10), ast.ID('z'))
            ),
            ast.Assignment(
                ast.ID('sum_times_five'),
                ast.BinOp(
                    '*',
                    ast.BinOp('+', ast.ID('x'), ast.ID('y')),
                    ast.Integer(5)
                )
            )
        ])

        assert result == expected
