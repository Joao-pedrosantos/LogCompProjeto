# parser.py

import ply.yacc as yacc
from lexer import tokens

# Variable dictionary
variaveis = {}

# Operator precedence
precedence = (
    ('left', 'IGUAL_IGUAL', 'MENOR', 'MAIOR'),
    ('left', 'MAIS', 'MENOS'),
    ('left', 'MULTIPLICACAO', 'DIVISAO'),
)

# Grammar definition
def p_programa(p):
    'programa : declaracoes'
    p[0] = ('programa', p[1])

def p_declaracoes(p):
    '''declaracoes : declaracao
                   | declaracoes declaracao'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaracao(p):
    '''declaracao : decl_var
                  | bloco_try_catch
                  | comando
                  | condicional
                  | func_call
                  | expressao_stmt'''
    p[0] = p[1]

def p_expressao_stmt(p):
    'expressao_stmt : expressao PONTO_VIRGULA'
    p[0] = ('expressao_stmt', p[1])

def p_decl_var(p):
    'decl_var : IDENTIFICADOR IGUAL expressao PONTO_VIRGULA'
    p[0] = ('decl_var', p[1], p[3])

def p_bloco_try_catch(p):
    '''bloco_try_catch : TRY DOIS_PONTOS bloco
                       | TRY DOIS_PONTOS bloco CATCH DOIS_PONTOS bloco'''
    if len(p) == 4:
        p[0] = ('try_catch', p[3], None)
    else:
        p[0] = ('try_catch', p[3], p[6])

def p_bloco(p):
    '''bloco : declaracao
             | bloco declaracao'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_condicional(p):
    '''condicional : IF ABRE_PARENTESE expressao FECHA_PARENTESE ABRE_CHAVE bloco FECHA_CHAVE
                   | IF ABRE_PARENTESE expressao FECHA_PARENTESE ABRE_CHAVE bloco FECHA_CHAVE ELSE ABRE_CHAVE bloco FECHA_CHAVE'''
    if len(p) == 8:
        # If without else
        p[0] = ('if', p[3], p[6], None)
    else:
        # If with else
        p[0] = ('if_else', p[3], p[6], p[10])

def p_comando(p):
    '''comando : acao PONTO_VIRGULA
               | acao ABRE_PARENTESE argumentos_opcionais FECHA_PARENTESE PONTO_VIRGULA
               | acao argumentos PONTO_VIRGULA'''
    if len(p) == 3:
        # Format: action ;
        p[0] = ('comando', p[1], None)
    elif p[2] == '(':
        # Format: action ( optional_arguments ) ;
        p[0] = ('comando', p[1], p[3])
    else:
        # Format: action arguments ;
        p[0] = ('comando', p[1], p[2])

def p_acao(p):
    '''acao : PRESS
            | EXIT
            | SHOW
            | TRYAGAIN'''
    p[0] = p[1]

def p_func_call(p):
    'func_call : IDENTIFICADOR ABRE_PARENTESE argumentos_opcionais FECHA_PARENTESE PONTO_VIRGULA'
    p[0] = ('func_call', p[1], p[3])

def p_argumentos_opcionais(p):
    '''argumentos_opcionais : argumentos
                            | empty'''
    if p[1] is None:
        p[0] = []
    else:
        p[0] = p[1]

def p_argumentos(p):
    '''argumentos : argumento
                  | argumentos VIRGULA argumento'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_argumento(p):
    '''argumento : expressao
                 | TECLA'''
    if p.slice[1].type == 'TECLA':
        p[0] = ('tecla', p[1])
    else:
        p[0] = p[1]

def p_expressao_binaria(p):
    '''expressao : expressao MAIS expressao
                 | expressao MENOS expressao
                 | expressao MULTIPLICACAO expressao
                 | expressao DIVISAO expressao'''
    p[0] = ('op_binaria', p[2], p[1], p[3])

def p_expressao_comparacao(p):
    '''expressao : expressao MENOR expressao
                 | expressao MAIOR expressao
                 | expressao IGUAL_IGUAL expressao'''
    p[0] = ('op_comparacao', p[2], p[1], p[3])

def p_expressao_paren(p):
    'expressao : ABRE_PARENTESE expressao FECHA_PARENTESE'
    p[0] = p[2]

def p_expressao_numero(p):
    'expressao : NUMERO'
    p[0] = ('numero', p[1])

def p_expressao_identificador(p):
    'expressao : IDENTIFICADOR'
    p[0] = ('var', p[1])

def p_expressao_string(p):
    'expressao : STRING'
    p[0] = ('string', p[1])

def p_empty(p):
    'empty :'
    pass

# Syntax error handling
def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}', linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo")

# Build the parser
parser = yacc.yacc()
