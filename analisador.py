# Alunos : Daniel A. B. V. Tannure - 2112182
#          Marina Magagnin - 1820698

import ply.lex as lex
import ply.yacc as yacc
import sys 

# ANÁLISE LÉXICA

# Nome dos tokens de operadores e constantes
reservados = ('INICIO', 
              'TERMINO', 
              'MONITOR',
              'EXECUTE', 
              'ENQUANTO', 
              'FACA', 
              'FIM', 
              'SOMA', 
              'MULT', 
              'ZERO', 
              'EVAL', 
              'IF', 
              'THEN',
              'ELSE', 
              'ABRE', 
              'FECHA', 
              'VIRGULA', 
              'MAIOR', 
              'MENOR', 
              'IGUAL',
              'variavel', 
              'numero')

# Expressões regulares para tokens de operadores e constantes
t_INICIO = r'INICIO'
t_TERMINO = r'TERMINO'
t_MONITOR = r'MONITOR'
t_EXECUTE = r'EXECUTE'
t_ENQUANTO = r'ENQUANTO'
t_FIM = r'FIM'
t_FACA = r'FACA'
t_SOMA = r'SOMA'
t_MULT = r'MULT'
t_ZERO = r'ZERO'
t_EVAL = r'EVAL'
t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_VIRGULA = r','
t_IGUAL = r'='
t_MAIOR = r'>'
t_MENOR = r'<'
t_ABRE = r'\('
t_FECHA= r'\)'

def t_variavel(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reservados:
        t.type = t.value
    return t

def t_numero(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'  # Ignora espaços e tabs

def t_error(t):  # Informa qual caractere é ilegal e se há erro
    print("Caractere ilegal: ", t.value[0])
    t.lexer.skip(1)

tokens = reservados

lexer = lex.lex(debug=True)

# ANÁLISE SINTÁTICA

# Tokens que já foram inicializados
inicializados = []
# Tokens a serem monitorados
monitorar = []

def p_regra_INICIO(regras):
    '''
    regra : INICIO varlist MONITOR monitorar EXECUTE cmds TERMINO
    '''
    # Formatação de string em formato de inicialização para C e encerramento do programa
    regras[0] = f"#include <stdio.h>\n\nint main(void) {{\n\t{regras[2]}\n\t{regras[6]}\n\treturn 0;\n}}"

def p_regra_cmds(regras):
    '''
    cmds : cmd
         | cmd cmds
    '''
    if len(regras) == 2:
        regras[0] = regras[1]
    else:
        regras[0] = f"{regras[1]}\n\t{regras[2]}"

def p_regra_cmd(regras):
    '''
    cmd : id IGUAL numero
        | id IGUAL id
        | funcao
        | IF condicao THEN cmd
        | ELSE cmd
        | ENQUANTO condicao FACA cmds FIM
        | EVAL ABRE id VIRGULA id VIRGULA cmds FECHA
        | EVAL ABRE numero VIRGULA numero VIRGULA cmds FECHA
    '''
    if len(regras) == 9:
        if (regras[3] in inicializados) and (regras[5] in inicializados):
            regras[0] = f"for (;{regras[3]}!={regras[5]} && {regras[3]} >{regras[5]};{regras[3]}--){{\n\t{regras[7]}\n}}"
        elif (type(regras[3]) is int) and (type(regras[5]) is int):
            #cria uma variável com a diferença dos número para o for
            regras[0] = f"int delta = {regras[3]} - {regras[5]};\n\tfor (int i = 0; i < delta && i >= 0; i++){{\n\t{regras[7]}\n}}"
        else:
            chamar_p_error(regras[3])
    elif len(regras) == 6:
        regras[0]= f"while({regras[2]}){{\n\t{regras[4]}\n\t}}"
    elif len(regras ) == 2:
        regras[0] = regras[1]
    elif regras[1] == 'IF':
        regras[0] = f"if ({regras[2]}) {{\n\t\t{regras[4]}\n\t}}"
    elif regras[1] == 'ELSE':
        regras[0] = f"else {{\n\t\t{regras[2]}\n\t}}"
    else:
        if regras[1] in monitorar:
            if regras[3] in monitorar:
                if (regras[1] in inicializados) and (regras[3] in inicializados):
                    regras[0] = f"{regras[1]} = {regras[3]};\n\tprintf(\"%d\", {regras[1]});\n\tprintf(\"%d\", {regras[3]});"
                elif regras[3] in inicializados:
                    inicializados.append(regras[1])
                    regras[0] = f"int {regras[1]} = {regras[3]};\n\tprintf(\"%d\", {regras[1]});\n\tprintf(\"%d\", {regras[3]});"
                else:
                    chamar_p_error(regras[3])             
            elif regras[1] in inicializados:
                if (type(regras[3]) is int) or (regras[3] in inicializados):
                    regras[0] = f"{regras[1]} = {regras[3]};\n\tprintf(\"%d\", {regras[1]});"
                else:
                    chamar_p_error(regras[3]) 
            else:
                if (type(regras[3]) is int) or (regras[3] in inicializados):
                    inicializados.append(regras[1])
                    regras[0] = f"int {regras[1]} = {regras[3]};\n\tprintf(\"%d\", {regras[1]});"
                else:
                    chamar_p_error(regras[3]) 
        else:
            if regras[1] in inicializados:
                if (type(regras[3]) is int) or (regras[3] in inicializados):
                    regras[0] = f"{regras[1]} = {regras[3]};"
                else:
                    chamar_p_error(regras[3])
            else:
                if (type(regras[3]) is int) or (regras[3] in inicializados):
                    inicializados.append(regras[1])
                    regras[0] = f"int {regras[1]} = {regras[3]};"
                else:
                    chamar_p_error(regras[3])

def p_regra_funcao(regras):
    '''
    funcao : SOMA ABRE id VIRGULA id FECHA
           | SOMA ABRE id VIRGULA numero FECHA
           | MULT ABRE id VIRGULA id FECHA
           | MULT ABRE id VIRGULA numero FECHA
           | id IGUAL MULT ABRE id VIRGULA
           | ZERO ABRE id FECHA
    '''

    if len(regras) == 5:
        if regras[3] in inicializados:
            if regras[3] in monitorar:
                regras[0] = f"{regras[3]} = 0;\n\tprintf(\"%d\", {regras[3]});"
            else:
                regras[0] = f"{regras[3]} = 0;"
        else:
            if regras[3] in monitorar:
                regras[0] = f"int {regras[3]} = 0;\n\tprintf(\"%d\", {regras[3]});"
            else:
                regras[0] = f"int {regras[3]} = 0;"
    elif len(regras) == 4:
        if regras[1] in inicializados:
            if regras[1] in monitorar:  
                regras[0]=f"{regras[1]} = {regras[3]};\n\tprintf(\"%d\", {regras[1]});"
            else:
                regras[0]=f"{regras[1]} = {regras[3]};"
        else:
            if regras[1] in monitorar:
                regras[0]=f"int {regras[1]} = {regras[3]};\n\tprintf(\"%d\", {regras[1]});"
            else:    
                regras[0]=f"int {regras[1]} = {regras[3]};"
    elif regras[1] == 'SOMA':
        if regras[3] in inicializados and ((regras[5] in inicializados) or (type(regras[5]) is int)):
            if regras[3] in monitorar:
                regras[0] = f"{regras[3]} = {regras[3]} + {regras[5]};\n\tprintf(\"%d\", {regras[3]});"
            else:
                regras[0] = f"{regras[3]} = {regras[3]} + {regras[5]};"
        elif ((regras[5] in inicializados) or (type(regras[5]) is int)):
            if regras[3] in monitorar:
                regras[0] = f"int {regras[3]} = {regras[3]} + {regras[5]};\n\tprintf(\"%d\", {regras[3]});"
            else:
                regras[0] = f" int{regras[3]} = {regras[3]} + {regras[5]};"
            inicializados.append(regras[3])
        else:
            print("oi")
            chamar_p_error(regras[3])
    elif regras[1] == 'MULT':
        if regras[3] in inicializados and ((regras[5] in inicializados) or (type(regras[5]) is int)):
            if regras[3] in monitorar:
                regras[0] = f"{regras[3]} = {regras[3]} * {regras[5]};\n\tprintf(\"%d\", {regras[3]});"
            else:
                regras[0] = f"{regras[3]} = {regras[3]} * {regras[5]};"
        elif ((regras[5] in inicializados) or (type(regras[5]) is int)):
            if regras[3] in monitorar:
                regras[0] = f"int {regras[3]} = {regras[3]} * {regras[5]};\n\tprintf(\"%d\", {regras[3]});"
            else:
                regras[0] = f" int {regras[3]} = {regras[3]} * {regras[5]};"
            inicializados.append(regras[3])

        else:
            chamar_p_error(regras[3])
        

#condição não aceita inicialização de variável na condição
def p_regra_condicao(regras):
    '''
    condicao : numero MAIOR id
             | numero MENOR id
             | numero IGUAL IGUAL id
             | id IGUAL IGUAL id
             | id IGUAL IGUAL numero
             | id MAIOR id
             | id MENOR id
             | id MAIOR numero
             | id MENOR numero
             | id
    '''
    if len(regras) == 2:
        if regras[1] in inicializados:
            regras[0] = regras[1]
        else:
            chamar_p_error(regras[1])
    elif len(regras) == 4:  # Para condições simples, como X > 3
        if (regras[1] in inicializados or type(regras[1]) is int) and (regras[3] in inicializados or type(regras[3]) is int):
            regras[0] = f"{regras[1]} {regras[2]} {regras[3]}"
        else:
            chamar_p_error(regras[1])
    elif len(regras) == 5:  # Para condições como X == Y
        if (regras[2] == '=' and regras[3] == '='):
            if (regras[1] in inicializados or type(regras[1]) is int) and (regras[4] in inicializados or type(regras[4]) is int):
                if not (type(regras[1]) is int and type(regras[4]) is int):  # Impede numero IGUAL IGUAL numero
                    regras[0] = f"{regras[1]} == {regras[4]}"
                else:
                    chamar_p_error(regras[1])
            else:
                chamar_p_error(regras[1])
    else:
        chamar_p_error(regras[1])


def p_regra_monitorar(regras):
    '''
    monitorar : id
              | id VIRGULA monitorar
    '''
    if len(regras) == 2:
        monitorar.append(regras[1])
        regras[0] = ""
    else:
        monitorar.append(regras[1])
        regras[0] = regras[3]

def p_regra_varlist(regras):
    '''
    varlist : id
            | id VIRGULA varlist
    '''
    if len(regras) == 2:
        inicializados.append(regras[1])
        regras[0] = f"int {regras[1]};"
    else:
        inicializados.append(regras[1])
        regras[0] = f"int {regras[1]};\n\t{regras[3]}"

def p_regra_id(regras):
    '''
    id : variavel
    '''
    regras[0] = regras[1]

# Função para chamar p_error manualmente
def chamar_p_error(token_value):
    fake_token = yacc.YaccSymbol()
    fake_token.value = token_value
    p_error(fake_token)

def p_error(regras):
    if regras:
        print(f"Erro de sintaxe em '{regras.value}'")
    else:
        print("Erro de sintaxe em entrada inesperada")
    sys.exit()

parser = yacc.yacc(debug=True, write_tables=True)

leitura = input("Digite o código:")
resultado = parser.parse(leitura)
print("Resultado:", resultado)
print("Monitorar:", monitorar)
print("Inicializados:", inicializados)
