from lexer import Lexer, LexerError


def main():
    print("=" * 50)
    print("       COMPILADOR MINI-LISP")
    print("=" * 50)

    codigo = """
    (begin
        (set x 10)
        (print x)
    )
    """

    print("\nCódigo fonte:")
    print(codigo)

    print("Tokens:")
    print("-" * 50)

    try:
        lexer = Lexer(codigo)
        tokens = lexer.tokenize()

        for token in tokens:
            print(token)

    except LexerError as error:
        print(error)


if __name__ == "__main__":
    main()