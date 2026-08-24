from lexer import Lexer, LexerError


def mostrar_tokens(tokens):
    print("\nLISTA DE TOKENS")
    print("=" * 45)
    print(f"{'LINHA':<8}{'NUM':<8}{'TOKEN':<18}{'LEXEMA'}")
    print(f"{'=====':<8}{'===':<8}{'=====':<18}{'======'}")

    numero = 1

    # Organizador dos tokens -----------------------------------------
    for token in tokens:
        if token.type.value == "EOF":
            continue

        # Formatação
        print(
            f"{token.line:<8}"
            f"{numero:<8}"
            f"{token.type.value:<18}"
            f"{token.lexeme}"
        )

        numero += 1

    print("=" * 45)


def main():
    print("=" * 50)
    print("           COMPILADOR MINI-LISP")
    print("=" * 50)

    # Código teste -----------------------------------------
    codigo = """ (print 10)
    """

    print("\nCódigo fonte:")
    print(codigo)

    try:
        lexer = Lexer(codigo)
        tokens = lexer.tokenize()
        # Analisa o código teste dentro do compilador, gerando os tokens.

        mostrar_tokens(tokens)

    except LexerError as error:
        print(error)


if __name__ == "__main__":
    main()