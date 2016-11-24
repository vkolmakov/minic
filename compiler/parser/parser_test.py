import unittest
from rply import Token

from compiler.parser.parser import Parser
import compiler.parser.ast as ast


parser = Parser()


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

    def test_relational_op_order(self):
        '''Relational ops have lowest precedence: `3 * 5 + 3 == 18;`'''
        given = iter([
            Token('INTEGER', '3'),
            Token('MUL', '*'),
            Token('INTEGER', '5'),
            Token('PLUS', '+'),
            Token('INTEGER', '3'),
            Token('EQUAL_EQUAL', '=='),
            Token('INTEGER', '18'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Statement(
                ast.BinOp(
                    '==',
                    ast.BinOp(
                        '+',
                        ast.BinOp('*', ast.Integer(3), ast.Integer(5)),
                        ast.Integer(3)
                    ),
                    ast.Integer(18)
                )
            )
        ])

        assert result == expected

    def test_simple_id(self):
        '''IDs are treated as expressions: `x;`'''
        given = iter([
            Token('ID', 'x'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Statement(
                ast.ID('x')
            )
        ])

        assert result == expected

    def test_mixed_expression(self):
        '''An expression can have both numbers and ids:
           `x * (y + 10);`'''
        given = iter([
            Token('ID', 'x'),
            Token('MUL', '*'),
            Token('LPAREN', '('),
            Token('ID', 'y'),
            Token('PLUS', '+'),
            Token('INTEGER', '10'),
            Token('RPAREN', ')'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Statement(
                ast.BinOp(
                    '*',
                    ast.ID('x'),
                    ast.BinOp('+', ast.ID('y'), ast.Integer(10))
                )
            )
        ])

        assert result == expected

    def test_arrayref_expression(self):
        '''Array reference is an expression: `arr[1];`'''
        given = iter([
            Token('ID', 'arr'),
            Token('LBRACE', '['),
            Token('INTEGER', '1'),
            Token('RBRACE', ']'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Statement(
                ast.ArrayRef(ast.ID('arr'), ast.Integer(1))
            )
        ])

        assert result == expected

    def test_float_expression(self):
        '''Expression with floats and integers: `1.0 + 2;`'''
        given = iter([
            Token('FLOAT', '1.0'),
            Token('PLUS', '+'),
            Token('INTEGER', '2'),
            Token('SEMI', ';')
        ])

        result = parser.parse(given)

        expected = ast.Block([
            ast.Statement(
                ast.BinOp(
                    '+',
                    ast.Float(1.0),
                    ast.Integer(2)
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

    def test_multiline_assignment(self):
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


class TestDeclaration(unittest.TestCase):
    def test_simple_declaration(self):
        '''Can parse a simple declaration: `int a;`'''
        given = iter([
            Token('INT_TYPE', 'int'),
            Token('ID', 'a'),
            Token('SEMI', ';')
        ])

        expected = ast.Block([
            ast.Declaration('int', [ast.ID('a')])
        ])

        result = parser.parse(given)

        assert expected == result

    def test_multiple_declaration(self):
        '''Can parse multiple declaration: `int ducks, and, wildcats;`'''
        given = iter([
            Token('INT_TYPE', 'int'),
            Token('ID', 'ducks'),
            Token('COMMA', ','),
            Token('ID', 'and'),
            Token('COMMA', ','),
            Token('ID', 'wildcats'),
            Token('SEMI', ';')
        ])

        expected = ast.Block([
            ast.Declaration(
                'int',
                [ast.ID('ducks'), ast.ID('and'), ast.ID('wildcats')]
            )
        ])

        result = parser.parse(given)

        assert expected == result


class TestBlockStatement(unittest.TestCase):
    def test_simple_block_of_statements(self):
        '''Can parse a nested block of statements:
           `int x;
            {
              int y;
              x = 5;
            }`
        '''
        given = iter([
            Token('INT_TYPE', 'int'),
            Token('ID', 'x'),
            Token('SEMI', ';'),

            Token('LCURLY', '{'),
            Token('INT_TYPE', 'int'),
            Token('ID', 'y'),
            Token('SEMI', ';'),
            Token('ID', 'x'),
            Token('EQUAL', '='),
            Token('INTEGER', '5'),
            Token('SEMI', ';'),
            Token('RCURLY', '}'),
        ])

        expected = ast.Block([
            ast.Declaration('int', [ast.ID('x')]),
            ast.Block([
                ast.Declaration('int', [ast.ID('y')]),
                ast.Assignment(ast.ID('x'), ast.Integer(5))
            ])
        ])

        result = parser.parse(given)

        assert expected == result


class TestIfStatement(unittest.TestCase):
    def test_single_if_statement(self):
        '''Can parse a single if statement
           `if (1) {
              duck = 3;
            }`
        '''
        given = iter([
            Token('IF', 'if'),
            Token('LPAREN', '('),
            Token('INTEGER', '1'),
            Token('RPAREN', ')'),

            Token('LCURLY', '{'),
            Token('ID', 'duck'),
            Token('EQUAL', '='),
            Token('INTEGER', '3'),
            Token('SEMI', ';'),
            Token('RCURLY', '}'),
        ])

        expected = ast.Block([
            ast.IfStatement(
                ast.Integer(1),
                ast.Block([
                    ast.Assignment(ast.ID('duck'), ast.Integer(3))
                ]),
                ast.Block([])
            )
        ])

        result = parser.parse(given)

        assert expected == result

    def test_if_else_statement(self):
        '''Can parse an if-else statement
           `if (x + 3) {
              duck = x;
            } else {
              goose = x;
            }`
        '''
        given = iter([
            Token('IF', 'if'),
            Token('LPAREN', '('),
            Token('ID', 'x'),
            Token('PLUS', '+'),
            Token('INTEGER', '3'),
            Token('RPAREN', ')'),

            Token('LCURLY', '{'),
            Token('ID', 'duck'),
            Token('EQUAL', '='),
            Token('ID', 'x'),
            Token('SEMI', ';'),
            Token('RCURLY', '}'),

            Token('ELSE', 'else'),

            Token('LCURLY', '{'),
            Token('ID', 'goose'),
            Token('EQUAL', '='),
            Token('ID', 'x'),
            Token('SEMI', ';'),
            Token('RCURLY', '}'),
        ])

        expected = ast.Block([
            ast.IfStatement(
                ast.BinOp('+', ast.ID('x'), ast.Integer(3)),
                ast.Block([
                    ast.Assignment(ast.ID('duck'), ast.ID('x'))
                ]),
                ast.Block([
                    ast.Assignment(ast.ID('goose'), ast.ID('x'))
                ])
            )
        ])

        result = parser.parse(given)

        assert expected == result


class TestParser(unittest.TestCase):
    def test_simple_program(self):
        '''Can parse a simple program
           `int x[3], duck, goose, wildcat;

            duck = 1;
            goose = 2;

            x[0] = duck;
            x[duck] = goose;

            if (duck + x[duck]) {
              wildcat = duck;
            } else {
              wildcat = goose;
            }
            x[2] = wildcat;`
        '''
        given = iter([
            Token('INT_TYPE', 'int'),
            Token('ID', 'x'), Token('LBRACE', '['), Token('INTEGER', '3'), Token('RBRACE', ']'), Token('COMMA', ','),
            Token('ID', 'duck'), Token('COMMA', ','),
            Token('ID', 'goose'), Token('COMMA', ','),
            Token('ID', 'wildcat'), Token('SEMI', ';'),

            Token('ID', 'duck'), Token('EQUAL', '='), Token('INTEGER', '1'), Token('SEMI', ';'),
            Token('ID', 'goose'), Token('EQUAL', '='), Token('INTEGER', '2'), Token('SEMI', ';'),
            Token('ID', 'x'), Token('LBRACE', '['), Token('INTEGER', '0'), Token('RBRACE', ']'), Token('EQUAL', '='), Token('ID', 'duck'), Token('SEMI', ';'),
            Token('ID', 'x'), Token('LBRACE', '['), Token('ID', 'duck'), Token('RBRACE', ']'), Token('EQUAL', '='), Token('ID', 'goose'), Token('SEMI', ';'),
            Token('IF', 'if'), Token('LPAREN', '('), Token('ID', 'duck'), Token('PLUS', '+'), Token('ID', 'x'), Token('LBRACE', '['), Token('ID', 'duck'), Token('RBRACE', ']'), Token('RPAREN', ')'),
            Token('LCURLY', '{'), Token('ID', 'wildcat'), Token('EQUAL', '='), Token('ID', 'duck'), Token('SEMI', ';'), Token('RCURLY', '}'),
            Token('ELSE', 'else'), Token('LCURLY', '{'), Token('ID', 'wildcat'), Token('EQUAL', '='), Token('ID', 'goose'), Token('SEMI', ';'), Token('RCURLY', '}'),
            Token('ID', 'x'), Token('LBRACE', '['), Token('INTEGER', '2'), Token('RBRACE', ']'), Token('EQUAL', '='), Token('ID', 'wildcat'), Token('SEMI', ';')
        ])

        expected = ast.Block([
            ast.Declaration(
                'int',
                [ast.ArrayRef(ast.ID('x'), ast.Integer(3)), ast.ID('duck'), ast.ID('goose'), ast.ID('wildcat')]
            ),
            ast.Assignment(ast.ID('duck'), ast.Integer(1)),
            ast.Assignment(ast.ID('goose'), ast.Integer(2)),

            ast.Assignment(ast.ArrayRef(ast.ID('x'), ast.Integer(0)), ast.ID('duck')),
            ast.Assignment(ast.ArrayRef(ast.ID('x'), ast.ID('duck')), ast.ID('goose')),

            ast.IfStatement(
                ast.BinOp('+', ast.ID('duck'), ast.ArrayRef(ast.ID('x'), ast.ID('duck'))),
                ast.Block([
                    ast.Assignment(ast.ID('wildcat'), ast.ID('duck'))
                ]),
                ast.Block([
                    ast.Assignment(ast.ID('wildcat'), ast.ID('goose'))
                ])
            ),

            ast.Assignment(ast.ArrayRef(ast.ID('x'), ast.Integer(2)), ast.ID('wildcat')),
        ])

        result = parser.parse(given)

        assert expected == result
