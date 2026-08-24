from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

    NUMBER = "NUMBER"
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


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int

    def __str__(self):
        return f"{self.type.value:<12} {self.lexeme:<15} linha {self.line}"