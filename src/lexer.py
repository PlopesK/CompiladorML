from tokens import Token, TokenType


class LexerError(Exception):
    pass


class Lexer:

    KEYWORDS = {
        "begin": TokenType.BEGIN,
        "set": TokenType.SET,
        "print": TokenType.PRINT,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
    }

    SYMBOLS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.MULTIPLY,
        "/": TokenType.DIVIDE,
        ">": TokenType.GREATER,
        "<": TokenType.LESS,
        "=": TokenType.EQUAL,
    }

    def __init__(self, source):

        self.source = source
        self.position = 0
        self.line = 1
        self.tokens = []

    def tokenize(self):

        while not self.is_at_end():

            char = self.advance()

            if char in " \t\r":
                continue

            if char == "\n":
                self.line += 1
                continue

            if char == "(":
                self.add_token(TokenType.LPAR, char)
                continue

            if char == ")":
                self.add_token(TokenType.RPAR, char)
                continue

            if char.isdigit():
                self.number()
                continue

            if char.isalpha() or char == "_":
                self.identifier()
                continue

            # Operadores ----------------------------------------
            # < && <=
            if char == "<":

                if self.peek() == "=":

                    self.advance()

                    self.add_token(
                        TokenType.LESS_EQUAL,
                        "<="
                    )

                else:

                    self.add_token(
                        TokenType.LESS,
                        "<"
                    )

                continue

            # > && >=
            if char == ">":
            
                if self.peek() == "=":

                    self.advance()

                    self.add_token(
                        TokenType.GREATER_EQUAL,
                        ">="
                    )

                else:

                    self.add_token(
                        TokenType.GREATER,
                        ">"
                    )

                continue

            # = && ==
            if char == "=":
            
                if self.peek() == "=":

                    self.advance()

                    self.add_token(
                        TokenType.EQUALITY,
                        "=="
                    )

                else:

                    self.add_token(
                        TokenType.EQUAL,
                        "="
                    )

                continue

            # !
            if char == "!":
                        
                if self.peek() == "=":

                    self.advance()

                    self.add_token(
                        TokenType.INEQUALITY,
                        "!="
                    )

                else:
                    raise LexerError(
                        f"Erro Léxico: Caractere inválido "
                        f"'!' na linha {self.line}."
                    )

                continue

            # Adicionar símbolos ----------------------------------------
            if char in self.SYMBOLS:

                self.add_token(
                    self.SYMBOLS[char],
                    char
                )

                continue

            raise LexerError(
                f"Erro Léxico: Caractere inválido "
                f"'{char}' na linha {self.line}."
            )

        self.tokens.append(
            Token(
                TokenType.EOF,
                "",
                self.line
            )
        )

        return self.tokens

    def number(self):

        start = self.position - 1

        while (
            not self.is_at_end()
            and self.peek().isdigit()
        ):
            self.advance()

        lexeme = self.source[start:self.position]

        self.add_token(
            TokenType.INTEGER,
            lexeme
        )

    def identifier(self):

        start = self.position - 1

        while not self.is_at_end():

            char = self.peek()

            if char.isalnum() or char == "_":
                self.advance()

            else:
                break

        lexeme = self.source[start:self.position]

        token_type = self.KEYWORDS.get(
            lexeme,
            TokenType.IDENTIFIER
        )

        self.add_token(
            token_type,
            lexeme
        )

    def add_token(self, token_type, lexeme):

        self.tokens.append(
            Token(
                token_type,
                lexeme,
                self.line
            )
        )

    def advance(self):

        char = self.source[self.position]

        self.position += 1

        return char

    def peek(self):

        if self.is_at_end():
            return "\0"

        return self.source[self.position]

    def is_at_end(self):

        return self.position >= len(self.source)