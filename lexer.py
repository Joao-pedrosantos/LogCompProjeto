# lexer.py

import ply.lex as lex

# List of token names
tokens = (
    'IDENTIFICADOR',
    'NUMERO',
    'STRING',
    'TECLA',
    'IGUAL',
    'PONTO_VIRGULA',
    'DOIS_PONTOS',
    'VIRGULA',
    'ABRE_PARENTESE',
    'FECHA_PARENTESE',
    'ABRE_CHAVE',
    'FECHA_CHAVE',
    'MAIS',
    'MENOS',
    'MULTIPLICACAO',
    'DIVISAO',
    'MENOR',
    'MAIOR',
    'IGUAL_IGUAL',
    # Reserved words
    'TRY',
    'CATCH',
    'PRESS',
    'EXIT',
    'SHOW',
    'TRYAGAIN',
    'IF',
    'ELSE',
)

# Reserved words mapping
reserved = {
    'try': 'TRY',
    'catch': 'CATCH',
    'press': 'PRESS',
    'exit': 'EXIT',
    'show': 'SHOW',
    'tryagain': 'TRYAGAIN',
    'if': 'IF',
    'else': 'ELSE',
}

# Regular expression rules for simple tokens
t_IGUAL          = r'='
t_PONTO_VIRGULA  = r';'
t_DOIS_PONTOS    = r':'
t_VIRGULA        = r','
t_ABRE_PARENTESE = r'\('
t_FECHA_PARENTESE= r'\)'
t_ABRE_CHAVE     = r'\{'
t_FECHA_CHAVE    = r'\}'
t_MAIS           = r'\+'
t_MENOS          = r'-'
t_MULTIPLICACAO  = r'\*'
t_DIVISAO        = r'/'
t_MENOR          = r'<'
t_MAIOR          = r'>'
t_IGUAL_IGUAL    = r'=='

# Ignore spaces, tabs, and carriage returns
t_ignore = ' \t\r'

# Ignore single-line comments
def t_COMMENT(t):
    r'//.*'
    pass

# Complex token definitions
def t_TECLA(t):
    r'[A-Z]+'
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove the quotes
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Check if the token is a reserved word
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}', linha {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
