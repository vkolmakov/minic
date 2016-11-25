import compiler.parser.ast as ast


class Typechecker:
    class SymbolTable:
        def __init__(self):
            self.declarations = {}  # str -> str, contains ids to types
            self.assignments = []  # list(ast.Assignment)

        def add_declaration(self, ast_declaration):
            for ast_id in ast_declaration.ids:
                self.declarations[ast_id.name] = ast_declaration.type

        def add_assignment(self, ast_assignment):
            self.assignments += [ast_assignment]

        def get_id_type(self, ast_id):
            return self.declarations[ast_id.name]

        def get_expression_type(self, ast_expr):
            if type(ast_expr) is ast.Float:
                return 'float'
            elif type(ast_expr) is ast.Integer:
                return 'int'

    def typecheck(self, tree):
        error_report = TypecheckerReport()
        symbol_table = Typechecker.SymbolTable()

        def typecheck_rec(node):
            if type(node) is ast.Assignment:
                expression_type = symbol_table.get_expression_type(node.expr)
                id_type = symbol_table.get_id_type(node.id)
                if expression_type != id_type:
                    error_report.add_error(node)
                symbol_table.add_assignment(node)
            elif type(node) is ast.Declaration:
                symbol_table.add_declaration(node)

        for node in tree.statements:
            typecheck_rec(node)

        print(symbol_table.declarations, symbol_table.assignments)
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
