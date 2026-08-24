from dataclasses import dataclass
from enum import Enum


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
    WHILE = "WHILE"

    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"

    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"

    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"

    EQUAL = "EQUAL"
    EQUALITY = "EQUALITY"
    INEQUALITY = "INEQUALITY"

    EOF = "EOF"


@dataclass
class Token:

    type: TokenType
    lexeme: str
    line: int

    def __str__(self):
        return (
            f"{self.type.value:<12} "
            f"{self.lexeme:<15} "
            f"linha {self.line}"
        )