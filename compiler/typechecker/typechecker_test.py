import unittest
from itertools import zip_longest

from compiler.typechecker.typechecker import (Typechecker, TypecheckerError)
import compiler.parser.ast as ast


typechecker = Typechecker()


class TestTypecheckerExpressions(unittest.TestCase):
    def test_simple_correct(self):
        '''No errors with given program:
           `int cowbell;
            cowbell = 2000;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('cowbell')]),
            ast.Assignment(ast.ID('cowbell'), ast.Integer(2000))
        ])

        report = typechecker.typecheck(given)
        expected_errors = []

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_simple_error(self):
        '''An error with given program:
           `int cowbell;
            cowbell = 2000.0;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('cowbell')]),
            ast.Assignment(ast.ID('cowbell'), ast.Float(2000.0))
        ])

        report = typechecker.typecheck(given)
        expected_errors = [
            TypecheckerError(
                ast.Assignment(ast.ID('cowbell'), ast.Float(2000.0))
            )
        ]

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_binop_correct(self):
        '''An error with given program:
           `int more_cowbell;
            more_cowbell = 2000 + 1;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('more_cowbell')]),
            ast.Assignment(
                ast.ID('more_cowbell'),
                ast.BinOp('+', ast.Integer(2000), ast.Integer(1))
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = []

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_binop_error(self):
        '''An error with given program:
           `int more_cowbell;
            more_cowbell = 2000.0 + 1;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('more_cowbell')]),
            ast.Assignment(
                ast.ID('more_cowbell'),
                ast.BinOp('+', ast.Float(2000.0), ast.Integer(1))
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = [
            TypecheckerError(
                ast.Assignment(
                    ast.ID('more_cowbell'),
                    ast.BinOp('+', ast.Float(2000.0), ast.Integer(1))
                )
            )
        ]

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_unary_op_correct(self):
        '''No errors with given program:
           `int negative_cowbell;
            negative_cowbell = -2000;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('negative_cowbell')]),
            ast.Assignment(
                ast.ID('negative_cowbell'),
                ast.UnaryOp('-', ast.Integer(2000))
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = []

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_unary_op_error(self):
        '''An error with given program:
           `int negative_cowbell;
            negative_cowbell = -2000.00;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('negative_cowbell')]),
            ast.Assignment(
                ast.ID('negative_cowbell'),
                ast.UnaryOp('-', ast.Float(2000.00))
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = [
            TypecheckerError(
                ast.Assignment(
                    ast.ID('negative_cowbell'),
                    ast.UnaryOp('-', ast.Float(2000.00))
                )
            )
        ]

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_id_expr_correct(self):
        '''No error with given program:
           `int ducks, wildcats;
            ducks = 100;
            wildcats = 200 % ducks;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('ducks'), ast.ID('wildcats')]),
            ast.Assignment(ast.ID('ducks'), ast.Integer(100)),
            ast.Assignment(
                ast.ID('wildcats'),
                ast.BinOp('%', ast.Integer(200), ast.ID('ducks'))
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = []

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_id_expr_error(self):
        '''No error with given program:
           `int ducks;
            float wildcats;
            ducks = 100;
            wildcats = 200 % ducks;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('ducks')]),
            ast.Declaration('float', [ast.ID('wildcats')]),
            ast.Assignment(ast.ID('ducks'), ast.Integer(100)),
            ast.Assignment(
                ast.ID('wildcats'),
                ast.BinOp('%', ast.Integer(200), ast.ID('ducks'))
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = [
            TypecheckerError(
                ast.Assignment(
                    ast.ID('wildcats'),
                    ast.BinOp('%', ast.Integer(200), ast.ID('ducks'))
                )
            )
        ]

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_arrayref_expr_correct(self):
        '''No error with given program:
           `int x[3];
            x[0] = 1;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ArrayRef(ast.ID('x'), ast.Integer(3))]),
            ast.Assignment(
                ast.ArrayRef(ast.ID('x'), ast.Integer(0)),
                ast.Integer(1)
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = []

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_arrayref_expr_error(self):
        '''An error with given program:
           `int x[3];
            x[0] = 1.0;`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ArrayRef(ast.ID('x'), ast.Integer(3))]),
            ast.Assignment(
                ast.ArrayRef(ast.ID('x'), ast.Integer(0)),
                ast.Float(1)
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = [
            TypecheckerError(
                ast.Assignment(
                    ast.ArrayRef(ast.ID('x'), ast.Integer(0)),
                    ast.Float(1)
                )
            )
        ]

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_if_statement_correct(self):
        '''No error with given program:
           `int x;
            if (x) {
              x = 1;
            } else {
              x = 0;
            }`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('x')]),
            ast.IfStatement(
                ast.ID('x'),
                ast.Block([
                    ast.Assignment(ast.ID('x'), ast.Integer(1))
                ]),
                ast.Block([
                    ast.Assignment(ast.ID('x'), ast.Integer(0))
                ]),
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = []

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_if_statement_error(self):
        '''An error with given program:
           `int x;
            if (x) {
              x = 1.0;
            } else {
              x = 0;
            }`'''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('x')]),
            ast.IfStatement(
                ast.ID('x'),
                ast.Block([
                    ast.Assignment(ast.ID('x'), ast.Float(1.0))
                ]),
                ast.Block([
                    ast.Assignment(ast.ID('x'), ast.Integer(0))
                ]),
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = [
            TypecheckerError(
                ast.Assignment(ast.ID('x'), ast.Float(1.0))
            )
        ]

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e


class TestTypechecker(unittest.TestCase):
    def test_simple_program_correct(self):
        '''Can typecheck a simple program:
           `int wildcat, animals[2];
            float duck;

            wildcat = 1;
            duck = 1.0;

            if(duck) {
              animals[0] = wildcat;
              animals[1] = 2;
            } else {
              animals[0] = 1;
            }

            duck = (duck + 2.5) * 33.0 / 2.0;
            `
        '''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('wildcat'), ast.ArrayRef(ast.ID('animals'), ast.Integer(2))]),
            ast.Declaration('float', [ast.ID('duck')]),

            ast.Assignment(ast.ID('wildcat'), ast.Integer(1)),
            ast.Assignment(ast.ID('duck'), ast.Float(1.0)),

            ast.IfStatement(
                ast.ID('duck'),
                ast.Block([
                    ast.Assignment(
                        ast.ArrayRef(ast.ID('animals'), ast.Integer(0)),
                        ast.ID('wildcat')
                    ),
                    ast.Assignment(
                        ast.ArrayRef(ast.ID('animals'), ast.Integer(1)),
                        ast.Integer(2)
                    )
                ]),
                ast.Block([
                    ast.Assignment(
                        ast.ArrayRef(ast.ID('animals'), ast.Integer(0)),
                        ast.Integer(1)
                    )
                ])
            ),

            ast.Assignment(
                ast.ID('duck'),
                ast.BinOp(
                    '/',
                    ast.BinOp(
                        '*',
                        ast.BinOp('+', ast.ID('duck'), ast.Float(2.5)),
                        ast.Float(33.0)
                    ),
                    ast.Float(2.0)
                )
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = []

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e

    def test_simple_program_error(self):
        '''Can typecheck a simple program:
           `int wildcat, animals[2];
            float duck;

            wildcat = 1.0;
            duck = 1;

            if(duck) {
              animals[0] = duck;
              animals[1] = 2;
            } else {
              animals[0] = 1;
            }

            duck = (duck + 2) * 33.0 / 2.0;
            `
        '''

        given = ast.Block([
            ast.Declaration('int', [ast.ID('wildcat'), ast.ArrayRef(ast.ID('animals'), ast.Integer(2))]),
            ast.Declaration('float', [ast.ID('duck')]),

            ast.Assignment(ast.ID('wildcat'), ast.Float(1.0)),
            ast.Assignment(ast.ID('duck'), ast.Integer(1)),

            ast.IfStatement(
                ast.ID('duck'),
                ast.Block([
                    ast.Assignment(
                        ast.ArrayRef(ast.ID('animals'), ast.Integer(0)),
                        ast.ID('duck')
                    ),
                    ast.Assignment(
                        ast.ArrayRef(ast.ID('animals'), ast.Integer(1)),
                        ast.Float(2.0)
                    )
                ]),
                ast.Block([
                    ast.Assignment(
                        ast.ArrayRef(ast.ID('animals'), ast.Integer(0)),
                        ast.Integer(1)
                    )
                ])
            ),

            ast.Assignment(
                ast.ID('duck'),
                ast.BinOp(
                    '/',
                    ast.BinOp(
                        '*',
                        ast.BinOp('+', ast.ID('duck'), ast.Integer(2)),
                        ast.Float(33.0)
                    ),
                    ast.Float(2.0)
                )
            )
        ])

        report = typechecker.typecheck(given)
        expected_errors = [
            TypecheckerError(
                ast.Assignment(ast.ID('wildcat'), ast.Float(1.0)),
            ),
            TypecheckerError(
                ast.Assignment(ast.ID('duck'), ast.Integer(1)),
            ),
            TypecheckerError(
                ast.Assignment(
                    ast.ArrayRef(ast.ID('animals'), ast.Integer(0)),
                    ast.ID('duck')
                )
            ),
            TypecheckerError(
                ast.Assignment(
                    ast.ArrayRef(ast.ID('animals'), ast.Integer(1)),
                    ast.Float(2.0)
                )
            ),
            TypecheckerError(
                ast.Assignment(
                    ast.ID('duck'),
                    ast.BinOp(
                        '/',
                        ast.BinOp(
                            '*',
                            ast.BinOp('+', ast.ID('duck'), ast.Integer(2)),
                            ast.Float(33.0)
                        ),
                        ast.Float(2.0)
                    )
                )
            )
        ]

        for (r, e) in zip_longest(report.get_errors(), expected_errors):
            assert r == e
