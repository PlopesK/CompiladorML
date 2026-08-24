from dataclasses import dataclass

from tokens import TokenType

class ParserError(Exception):
    pass

# ===================== NÓS DA AST =====================

@dataclass
class NumberNode:
    value: int


@dataclass
class IdentifierNode:
    name: str


@dataclass
class BinaryOperationNode:
    operator: str
    left: object
    right: object


@dataclass
class SetNode:
    name: str
    expression: object


@dataclass
class PrintNode:
    expression: object


@dataclass
class BeginNode:
    expressions: list


@dataclass
class IfNode:
    condition: object
    then_branch: object
    else_branch: object


# ============================================================
# ANALISADOR SINTÁTICO
# ============================================================

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        expressions = []

        while not self.is_at_end():
            expressions.append(self.expression())

        return expressions

    # Expressões -----------------------------------------
    def expression(self):
        token = self.peek()

        if token.type == TokenType.INTEGER:
            self.advance()
            return NumberNode(int(token.lexeme))

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return IdentifierNode(token.lexeme)

        if token.type == TokenType.LPAR:
            return self.list_expression()

        raise ParserError(
            f"Erro Sintático na linha {token.line}: "
            f"Expressão inesperada '{token.lexeme}'."
        )

    # Listas -----------------------------------------
    def list_expression(self):
        self.consume(
            TokenType.LPAR,
            "Esperava-se '('."
        )

        token = self.peek()

        if token.type == TokenType.PRINT:
            return self.print_expression()

        if token.type == TokenType.SET:
            return self.set_expression()

        if token.type == TokenType.BEGIN:
            return self.begin_expression()

        if token.type == TokenType.IF:
            return self.if_expression()

        if token.type in {
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.EQUAL
        }:
            return self.binary_expression()

        raise ParserError(
            f"Erro Sintático na linha {token.line}: "
            f"Estrutura desconhecida '{token.lexeme}'."
        )

    # Print -----------------------------------------
    def print_expression(self):
        self.advance() #PRINT

        expression = self.expression()

        self.consume(
            TokenType.RPAR,
            "Esperava-se ')' após a expressão de print."
        )

        return PrintNode(expression)

    # Set -----------------------------------------
    def set_expression(self):
        self.advance()  # SET

        identifier = self.consume(
            TokenType.IDENTIFIER,
            "Esperava-se um identificador após 'set'."
        )

        expression = self.expression()

        self.consume(
            TokenType.RPAR,
            "Esperava-se ')' após a expressão de set."
        )

        return SetNode(
            identifier.lexeme,
            expression
        )

    # Begin -----------------------------------------
    def begin_expression(self):
        self.advance()  # BEGIN

        expressions = []

        while not self.check(TokenType.RPAR):

            if self.is_at_end():
                token = self.peek()

                raise ParserError(
                    f"Erro Sintático na linha {token.line}: "
                    f"Fim de arquivo inesperado. "
                    f"Esperava-se ')'."
                )

            expressions.append(self.expression())

        self.advance()  # RPAR

        if not expressions:
            raise ParserError(
                "Erro Sintático: 'begin' deve possuir "
                "pelo menos uma expressão."
            )

        return BeginNode(expressions)

    # If -----------------------------------------
    def if_expression(self):
        self.advance()  # IF

        condition = self.expression()

        then_branch = self.expression()

        if self.check(TokenType.RPAR):
            token = self.peek()

            raise ParserError(
                f"Erro Sintático na linha {token.line}: "
                "Estrutura 'if' malformada. "
                "Omitido argumento de 'else'."
            )

        else_branch = self.expression()

        self.consume(
            TokenType.RPAR,
            "Esperava-se ')' após a estrutura 'if'."
        )

        return IfNode(
            condition,
            then_branch,
            else_branch
        )

    # Operações Binárias -----------------------------------------
    def binary_expression(self):
        operator = self.advance()

        left = self.expression()
        right = self.expression()

        self.consume(
            TokenType.RPAR,
            f"Esperava-se ')' após a operação '{operator.lexeme}'."
        )

        return BinaryOperationNode(
            operator.lexeme,
            left,
            right
        )

    # Funções Auxiliares -----------------------------------------
    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        token = self.peek()

        raise ParserError(
            f"Erro Sintático na linha {token.line}: {message}"
        )

    def check(self, token_type):
        if self.is_at_end():
            return token_type == TokenType.EOF

        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def is_at_end(self):
        return self.peek().type == TokenType.EOF