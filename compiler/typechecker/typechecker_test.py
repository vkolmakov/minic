import unittest
from itertools import zip_longest

from compiler.typechecker.typechecker import (Typechecker, TypecheckerError)
import compiler.parser.ast as ast


typechecker = Typechecker()


class TestTypechecker(unittest.TestCase):
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
