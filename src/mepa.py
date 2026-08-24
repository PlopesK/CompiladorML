from parser import (
    NumberNode,
    IdentifierNode,
    BinaryOperationNode,
    SetNode,
    PrintNode,
    BeginNode,
    IfNode,
    WhileNode
)


class MEPAGenerator:

    def __init__(self, symbol_table):

        self.symbol_table = symbol_table
        self.code = []
        self.label_count = 1

    def emit(self, instruction):

        self.code.append(instruction)

    def new_label(self):

        label = f"R{self.label_count}"

        self.label_count += 1

        return label

    def generate(self, nodes):

        self.emit("INPP")

        for node in nodes:
            self.visit(node)

        self.emit("PARA")

        return self.code

    def visit(self, node):

        # Número
        if isinstance(node, NumberNode):

            self.emit(
                f"CRCT {node.value}"
            )

        # Variável
        elif isinstance(node, IdentifierNode):

            symbol = self.symbol_table.get(
                node.name
            )

            self.emit(
                f"CRVL {symbol.address}"
            )

        # Operações
        elif isinstance(node, BinaryOperationNode):

            self.visit(node.left)
            self.visit(node.right)

            if node.operator == "+":
                self.emit("SOMA")

            elif node.operator == "-":
                self.emit("SUBT")

            elif node.operator == "*":
                self.emit("MULT")

            elif node.operator == "/":
                self.emit("DIVI")

            elif node.operator == "<=":
                self.emit("CMME")

            elif node.operator == "<":
                self.emit("CMME")

            elif node.operator == ">":
                self.emit("CMMA")

            elif node.operator == "=":
                self.emit("CMIG")

        # Set
        elif isinstance(node, SetNode):

            self.visit(node.expression)

            symbol = self.symbol_table.get(
                node.name
            )

            self.emit(
                f"ARMZ {symbol.address}"
            )

        # Print
        elif isinstance(node, PrintNode):

            self.visit(node.expression)

            self.emit("IMPR")

        # Begin
        elif isinstance(node, BeginNode):

            for expression in node.expressions:

                self.visit(expression)

        # While
        elif isinstance(node, WhileNode):

            start = self.new_label()
            end = self.new_label()

            self.emit(
                f"{start}: NADA"
            )

            self.visit(node.condition)

            self.emit(
                f"DSVF {end}"
            )

            self.visit(node.body)

            self.emit(
                f"DSVS {start}"
            )

            self.emit(
                f"{end}: NADA"
            )

        # If
        elif isinstance(node, IfNode):

            else_label = self.new_label()
            end_label = self.new_label()

            self.visit(node.condition)

            self.emit(
                f"DSVF {else_label}"
            )

            self.visit(node.then_branch)

            self.emit(
                f"DSVS {end_label}"
            )

            self.emit(
                f"{else_label}: NADA"
            )

            self.visit(node.else_branch)

            self.emit(
                f"{end_label}: NADA"
            )

        else:

            raise Exception(
                f"Nó não suportado: "
                f"{type(node).__name__}"
            )

    def display(self):

        if not self.code:

            print("Código MEPA vazio")

            return

        print("\nGERAÇÃO DE CÓDIGO INTERMEDIÁRIO")

        print("=" * 50)

        for instruction in self.code:

            print(instruction)

        print("=" * 50)