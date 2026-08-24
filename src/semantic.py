from dataclasses import dataclass

class SemanticError(Exception):
    pass

@dataclass
class Symbol:
    name: str
    type: str
    scope: str
    address: int
    initialized: bool
    value: object = None

# ============================================================
# TABELA DE SÍMBOLOS
# ============================================================

class SymbolTable:

    def __init__(self):
        self.symbols = {}
        self.next_address = 0

    def define(
        self,
        name,
        symbol_type,
        scope="GLOBAL",
        value=None
    ):

        # Se a variável já existe,
        # mantém o endereço que ela já possuía
        if name in self.symbols:

            address = self.symbols[name].address

        else:

            address = self.next_address

            self.next_address += 1

        self.symbols[name] = Symbol(
            name=name,
            type=symbol_type,
            scope=scope,
            address=address,
            initialized=True,
            value=value
        )

    def exists(self, name):
        return name in self.symbols

    def get(self, name):
        return self.symbols.get(name)

    def display(self):
        if not self.symbols:

            print("Tabela vazia")
            print("=" * 65)

            return

        print("=" * 65)

        print(
            f"{'IDENTIFICADOR':<18}"
            f"{'ENDEREÇO MEPA':<18}"
            f"{'TIPO':<15}"
            f"{'ESCOPO'}"
        )

        print(
            f"{'=============':<18}"
            f"{'=============':<18}"
            f"{'====':<15}"
            f"{'======'}"
        )

        for symbol in self.symbols.values():

            print(
                f"{symbol.name:<18}"
                f"{symbol.address:<18}"
                f"{symbol.type:<15}"
                f"{symbol.scope}"
            )

        print("=" * 65)


# ============================================================
# ANALISADOR SEMÂNTICO
# ============================================================

class SemanticAnalyzer:

    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, nodes):

        for node in nodes:
            self.visit(node)

        return self.symbol_table

    # Número -----------------------------------------
    def visit_number(self, node):
        return "INTEGER"

    # Identificador -----------------------------------------
    def visit_identifier(self, node):

        if not self.symbol_table.exists(node.name):
            raise SemanticError(
                f"Erro Semântico: Variável "
                f"'{node.name}' não foi inicializada."
            )

        symbol = self.symbol_table.get(node.name)

        if not symbol.initialized:
            raise SemanticError(
                f"Erro Semântico: Variável "
                f"'{node.name}' não foi inicializada."
            )

        return symbol.type

    # Set -----------------------------------------
    def visit_set(self, node):

        expression_type = self.visit(node.expression)

        if expression_type != "INTEGER":
            raise SemanticError(
                f"Erro Semântico: Não é possível atribuir "
                f"o valor à variável '{node.name}'."
            )

        value = self.get_constant_value(node.expression)

        self.symbol_table.define(
            name=node.name,
            symbol_type=expression_type,
            scope="GLOBAL",
            value=value
        )

        return expression_type

    # Print -----------------------------------------
    def visit_print(self, node):

        self.visit(node.expression)

        return None

    # Operação Binária -----------------------------------------
    def visit_binary_operation(self, node):

        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != "INTEGER" or right_type != "INTEGER":
            raise SemanticError(
                f"Erro Semântico: Operação '{node.operator}' "
                f"requer operandos inteiros."
            )

        return "INTEGER"

    # Begin -----------------------------------------
    def visit_begin(self, node):

        for expression in node.expressions:
            self.visit(expression)

        return None

    # If -----------------------------------------
    def visit_if(self, node):

        condition_type = self.visit(node.condition)

        if condition_type != "INTEGER":
            raise SemanticError(
                "Erro Semântico: Condição do 'if' "
                "deve ser uma expressão inteira."
            )

        self.visit(node.then_branch)
        self.visit(node.else_branch)

        return None

    # While -----------------------------------------
    def visit_while(self, node):

        condition_type = self.visit(node.condition)

        if condition_type != "INTEGER":
            raise SemanticError(
                "Erro Semântico: Condição do 'while' "
                "deve ser uma expressão inteira."
            )

        self.visit(node.body)

        return None

    # Visitador -----------------------------------------
    def visit(self, node):

        if node.__class__.__name__ == "NumberNode":
            return self.visit_number(node)

        if node.__class__.__name__ == "IdentifierNode":
            return self.visit_identifier(node)

        if node.__class__.__name__ == "SetNode":
            return self.visit_set(node)

        if node.__class__.__name__ == "PrintNode":
            return self.visit_print(node)

        if node.__class__.__name__ == "BinaryOperationNode":
            return self.visit_binary_operation(node)

        if node.__class__.__name__ == "BeginNode":
            return self.visit_begin(node)

        if node.__class__.__name__ == "IfNode":
            return self.visit_if(node)

        if node.__class__.__name__ == "WhileNode":
            return self.visit_while(node)

        raise SemanticError(
            f"Erro Semântico: Tipo de nó desconhecido "
            f"'{node.__class__.__name__}'."
        )

    # Valores Constantes -----------------------------------------
    def get_constant_value(self, node):
        if node.__class__.__name__ == "NumberNode":
            return node.value

        if node.__class__.__name__ == "IdentifierNode":

            symbol = self.symbol_table.get(node.name)

            if symbol is not None:
                return symbol.value

            return None

        if node.__class__.__name__ == "BinaryOperationNode":

            left = self.get_constant_value(node.left)
            right = self.get_constant_value(node.right)

            if left is None or right is None:
                return None

            if node.operator == "+":
                return left + right

            if node.operator == "-":
                return left - right

            if node.operator == "*":
                return left * right

            if node.operator == "/":

                if right == 0:
                    raise SemanticError(
                        "Erro Semântico: Divisão por zero."
                    )

                return left // right

        return None