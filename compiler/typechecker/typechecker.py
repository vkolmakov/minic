import compiler.parser.ast as ast


class Typechecker:
    class SymbolTable:
        def __init__(self):
            self.declarations = {}  # str -> str, contains ids to types

        def add_declaration(self, ast_declaration):
            for ast_id in ast_declaration.ids:
                self.declarations[ast_id.name] = ast_declaration.type

        def get_id_type(self, ast_id):
            return self.declarations[ast_id.name]

        def get_expression_type(self, ast_expr):
            def get_expression_type_rec(node, types):
                if type(node) is ast.Float:
                    return ['float'] + types[:]
                elif type(node) is ast.Integer:
                    return ['int'] + types[:]
                elif type(node) is ast.ID:
                    return [self.get_id_type(node)] + types[:]
                elif type(node) is ast.BinOp:
                    return (get_expression_type_rec(node.left, types) +
                            get_expression_type_rec(node.right, types))
                elif type(node) is ast.UnaryOp:
                    return get_expression_type_rec(node.expr, types)
                else:
                    return types

            expr_types = get_expression_type_rec(ast_expr, [])
            if all(t == 'int' for t in expr_types):
                return 'int'
            elif all(t == 'float' for t in expr_types):
                return 'float'
            else:
                return None

    def typecheck(self, tree):
        error_report = TypecheckerReport()
        symbol_table = Typechecker.SymbolTable()

        def typecheck_rec(node):
            if type(node) is ast.Assignment:
                expression_type = symbol_table.get_expression_type(node.expr)
                id_type = symbol_table.get_id_type(node.id)
                if expression_type != id_type:
                    error_report.add_error(node)
            elif type(node) is ast.Declaration:
                symbol_table.add_declaration(node)

        for node in tree.statements:
            typecheck_rec(node)

        return error_report


class TypecheckerReport:
    def __init__(self):
        self.errors = []

    def get_errors(self):
        return self.errors

    def add_error(self, ast_node):
        self.errors += [TypecheckerError(ast_node)]


class TypecheckerError:
    def __init__(self, ast_node):
        self.ast_node = ast_node

    def __eq__(self, other):
        return (isinstance(other, TypecheckerError) and
                self.get_ast_node() == other.get_ast_node())

    def get_ast_node(self):
        return self.ast_node
