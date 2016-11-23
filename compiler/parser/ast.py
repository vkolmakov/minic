class AstNode:
    def __eq__(self, other):
        if not isinstance(other, AstNode):
            return False

        if not type(self) is type(other):
            return False

        for attr in list(self.__dict__):
            # get top-level attribute values
            self_data = self.__getattribute__(attr)
            other_data = other.__getattribute__(attr)

            if not type(self_data) is type(other_data):
                return False

            if hasattr(self_data, '__iter__') and hasattr(other_data, '__iter__'):
                # if attribute is an iterable, check all subitems in order
                for (self_subnode, other_subnode) in zip(self_data, other_data):
                    if self_subnode.__ne__(other_subnode):
                        return False
            elif self_data.__ne__(other_data):
                # if attribute if something else, check if they are equal
                return False

        return True

    def __ne__(self, other):
        return not (self == other)


class Block(AstNode):
    def __init__(self, statements):
        self.statements = statements


class Statement(AstNode):
    def __init__(self, expr):
        self.expr = expr


class Integer(AstNode):
    def __init__(self, value):
        self.value = value


class ID(AstNode):
    def __init__(self, name):
        self.name = name


class BinOp(AstNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Assignment(AstNode):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr