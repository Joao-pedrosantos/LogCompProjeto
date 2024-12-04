# interpreter.py

from lexer import lexer
from parser import parser, variaveis

# Necessary modules
import sys
import time
import pyautogui

# Custom exception for tryagain
class TryAgainException(Exception):
    pass

# Global variable to track if we are inside a catch block
dentro_catch = False

# Main function to interpret the program
def interpretar_programa(ast):
    if ast[0] == 'programa':
        interpretar_declaracoes(ast[1])

def interpretar_declaracoes(declaracoes):
    for declaracao in declaracoes:
        interpretar_declaracao(declaracao)

def interpretar_declaracao(declaracao):
    tipo = declaracao[0]
    if tipo == 'decl_var':
        interpretar_decl_var(declaracao)
    elif tipo == 'try_catch':
        interpretar_try_catch(declaracao)
    elif tipo == 'comando':
        interpretar_comando(declaracao)
    elif tipo == 'if':
        interpretar_condicional(declaracao)
    elif tipo == 'if_else':
        interpretar_condicional(declaracao)
    elif tipo == 'func_call':
        interpretar_func_call(declaracao)
    elif tipo == 'expressao_stmt':
        avaliar_expressao(declaracao[1])
    else:
        print(f"Declaração desconhecida: {tipo}")

def interpretar_decl_var(declaracao):
    _, nome_var, expressao = declaracao
    valor = avaliar_expressao(expressao)
    variaveis[nome_var] = valor

def interpretar_try_catch(declaracao):
    global dentro_catch
    _, bloco_try, bloco_catch = declaracao
    while True:
        try:
            interpretar_declaracoes(bloco_try)
            break  # Exit loop if try block succeeds
        except TryAgainException:
            # If tryagain() was called, the loop continues and the try block is re-executed
            continue
        except Exception as e:
            if bloco_catch:
                try:
                    dentro_catch = True  # Entering catch block
                    interpretar_declaracoes(bloco_catch)
                    dentro_catch = False  # Exiting catch block
                except TryAgainException:
                    dentro_catch = False
                    # If tryagain() is called in catch, restart the try block
                    continue
                break  # Exit loop after executing catch
            else:
                print(f"Erro não tratado: {e}")
                break

def interpretar_condicional(declaracao):
    tipo = declaracao[0]
    if tipo == 'if':
        _, condicao, bloco_then, _ = declaracao
        resultado = avaliar_expressao(condicao)
        if resultado:
            interpretar_declaracoes(bloco_then)
    elif tipo == 'if_else':
        _, condicao, bloco_then, bloco_else = declaracao
        resultado = avaliar_expressao(condicao)
        if resultado:
            interpretar_declaracoes(bloco_then)
        else:
            interpretar_declaracoes(bloco_else)

def interpretar_comando(comando):
    _, acao, argumentos = comando
    if acao == 'press':
        interpretar_press(argumentos)
    elif acao == 'exit':
        interpretar_exit(argumentos)
    elif acao == 'show':
        interpretar_show(argumentos)
    elif acao == 'tryagain':
        interpretar_tryagain(argumentos)
    else:
        print(f"Ação desconhecida: {acao}")

def interpretar_func_call(declaracao):
    _, func_name, argumentos = declaracao
    # Since 'error' is not a defined function, we can raise an exception to simulate an error
    if func_name == 'error':
        raise Exception('Simulated error')
    else:
        print(f"Função desconhecida: {func_name}")

def interpretar_press(argumentos):
    if not argumentos or len(argumentos) < 1:
        print("Erro: 'press' requer pelo menos um argumento.")
        return
    tecla = argumentos[0]
    if isinstance(tecla, tuple):
        tipo = tecla[0]
        if tipo == 'tecla':
            tecla = tecla[1]
        else:
            tecla = avaliar_expressao(tecla)
    else:
        tecla = str(tecla)
    tecla = tecla.lower()  # Convert the key to lowercase
    repeticoes = 1
    if len(argumentos) > 1:
        repeticoes = avaliar_expressao(argumentos[1])
    try:
        repeticoes = int(repeticoes)
    except ValueError:
        print("Erro: O número de repetições deve ser um inteiro.")
        return
    for _ in range(repeticoes):
        print(f"Pressionando tecla: {tecla}")
        try:
            pyautogui.press(tecla)
            time.sleep(0.1)  # Adjust the interval as needed
        except Exception as e:
            print(f"Erro ao pressionar a tecla '{tecla}': {e}")
            raise e  # Raise the exception so that 'try/catch' can handle it

def interpretar_exit(argumentos):
    print("Saindo do programa.")
    sys.exit()

def interpretar_show(argumentos):
    if not argumentos or len(argumentos) < 1:
        print("Erro: 'show' requer um argumento.")
        return
    mensagem = argumentos[0]
    if isinstance(mensagem, tuple):
        mensagem = avaliar_expressao(mensagem)
    print(mensagem)

def interpretar_tryagain(argumentos):
    if dentro_catch:
        raise TryAgainException()
    else:
        print("Erro: 'tryagain' só pode ser usado dentro de um bloco 'catch'.")

def avaliar_expressao(expressao):
    if isinstance(expressao, tuple):
        tipo = expressao[0]
        if tipo == 'op_binaria':
            op = expressao[1]
            esquerda = avaliar_expressao(expressao[2])
            direita = avaliar_expressao(expressao[3])
            if op == '+':
                # Handle string concatenation
                if isinstance(esquerda, str) or isinstance(direita, str):
                    return str(esquerda) + str(direita)
                else:
                    return esquerda + direita
            elif op == '-':
                return esquerda - direita
            elif op == '*':
                return esquerda * direita
            elif op == '/':
                return esquerda / direita
        elif tipo == 'op_comparacao':
            op = expressao[1]
            esquerda = avaliar_expressao(expressao[2])
            direita = avaliar_expressao(expressao[3])
            if op == '<':
                return esquerda < direita
            elif op == '>':
                return esquerda > direita
            elif op == '==':
                return esquerda == direita
        elif tipo == 'numero':
            return expressao[1]
        elif tipo == 'var':
            nome_var = expressao[1]
            if nome_var in variaveis:
                return variaveis[nome_var]
            else:
                # Instead of exiting, raise an exception
                raise Exception(f"Variável '{nome_var}' não definida.")
        elif tipo == 'string':
            return expressao[1]
        elif tipo == 'tecla':
            return expressao[1]
        else:
            print(f"Expressão desconhecida: {tipo}")
            raise Exception(f"Expressão desconhecida: {tipo}")
    else:
        return expressao
