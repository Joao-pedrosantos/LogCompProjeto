# main.py

import sys
from lexer import lexer
from parser import parser
from interpreter import interpretar_programa

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)
    arquivo = sys.argv[1]
    with open(arquivo, 'r', encoding='utf-8') as f:
        codigo_fonte = f.read()
    ast = parser.parse(codigo_fonte, lexer=lexer)
    if ast is not None:
        interpretar_programa(ast)
    else:
        print("Erro: Não foi possível gerar a árvore sintática abstrata (AST).")

if __name__ == '__main__':
    main()
