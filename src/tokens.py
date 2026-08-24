from dataclasses import dataclass
from enum import Enum

# Tipos de Token
class TokenType(Enum):
    LPAR = "LPAR"
    RPAR = "RPAR"

    INTEGER = "INTEGER"
    IDENTIFIER = "IDENTIFIER"

    BEGIN = "BEGIN"
    SET = "SET"
    PRINT = "PRINT"
    IF = "IF"
    ELSE = "ELSE"

    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"

    GREATER = "GREATER"
    LESS = "LESS"
    EQUAL = "EQUAL"

    EOF = "EOF"

# Criando um objeto(classe) para os tokens
@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int

    def __str__(self):
        return f"{self.type.value:<12} {self.lexeme:<15} linha {self.line}"