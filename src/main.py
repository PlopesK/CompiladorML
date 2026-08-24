from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from mepa import MEPAGenerator

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
    codigo = """(begin
    (set tempo 5)
    (while (> tempo 0)
        (begin
            (print tempo)
            (set tempo (- tempo 1))
        )
    )
    (print 0)
)"""

    print("\nCódigo fonte:")
    print(codigo)

    # Analisa o código teste dentro do compilador, gerando os tokens.
    try:
        # 1- ANÁLISE LÉXICA -------------------------------------
        lexer = Lexer(codigo)
        tokens = lexer.tokenize()

        mostrar_tokens(tokens)

        # 2- ANÁLISE SINTÁTICA -------------------------------------
        print("\nANÁLISE SINTÁTICA")
        print("=" * 55)

        parser = Parser(tokens)
        ast = parser.parse()

        print("Análise sintática concluída com sucesso!")
        print(f"Expressões encontradas: {len(ast)}")

        print("=" * 55)

        # 3- ANÁLISE SEMÂNTICA -------------------------------------
        print("\nANÁLISE SEMÂNTICA - TABELA DE SÍMBOLOS")

        semantic_analyzer = SemanticAnalyzer()

        symbol_table = semantic_analyzer.analyze(ast)

        symbol_table.display()

        # 4- GERAÇÃO DE CÓDIGO MEPA -------------------------------------
        generator = MEPAGenerator(
            symbol_table
        )

        generator.generate(ast)

        generator.display()

    # ERROS ----------------------------------------------------
    except LexerError as error:
        print(error)

    except ParserError as error:
        print(error)

    except SemanticError as error:
        print(error)

# Executa o Programa -----------------------------
if __name__ == "__main__":
    main()