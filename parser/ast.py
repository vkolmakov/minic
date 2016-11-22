class AstNode:
    def __eq__(self, other):
        pass


class Block(AstNode):
    def __init__(self, statements):
        self.statements = statements


class Statement(AstNode):
    def __init__(self, expr):
        self.expr = expr


class Number(AstNode):
    def __init__(self, value):
        self.value = value


class ID(AstNode):
    def __init__(self, name):
        self.name = name
