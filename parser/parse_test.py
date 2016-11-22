import unittest
from parser.parse import Parser

import parser.ast.primitives
import parser.ast.types


class TestPrimitives(unittest.TestCase):
    def test_id(self):
        result = Parser.parse('x;')
        pass

    def test_integer(self):
        pass

    def test_float(self):
        pass

    def test_arrayref(self):
        pass
