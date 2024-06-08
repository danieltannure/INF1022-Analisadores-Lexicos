import ply.lex as lex
import ply.yacc as yacc

#ANALISADOR LÉXICO

# nome dos tokens de operadores e constantes
reservados= ('INICIO','TERMINO','VIRGULA','variavel');

# expressões regulares para tokens de operadores e constantes

t_INICIO = r'INICIO'
t_TERMINO=r'TERMINO'
t_VIRGULA=r','

# como esse é o token mais expressivo, utilizamos essa 
# função para diferenciar as palavras reservadas dele

def t_variavel(t):
  r'[a-zA-Z_][a-zA-Z0-9_]*'
  if t.value in reservados: # igual
      t.type = t.value
  return t

# aqui definimos o token numero, ele nesse caso converte 
# o valor direto para um inteiro, mas poderia ser um float

t_ignore = ' \t\n' # ignora espaços e tabs

def t_error(t): # nos dizer qual caractere ilegal e se tem erro
  print("Caracter ilegal: ", t.value[0])
  t.lexer.skip(1)

tokens = reservados

lexer = lex.lex(debug=False)
#ANALISADOR SINTÁTICO

def p_regra_INICIO(regras):
  '''
  regra : INICIO  varlist TERMINO
  '''
  #formatação de string em formato de inicialização para C e encerreamento do programa
  regras[0]= f"#include <stdio.h> int main(void) {{ {regras[2]} return 0;}}"  

def p_regra_varlist(regras):
  '''
  varlist : id
          | id VIRGULA varlist
  '''
  
  if len(regras) == 2:
    #se so tiver um id, ele é inserido no formato de inicialização
    regras[0]= f"int {regras[1]};"
  else:
    #caso tenha mais, ele inicializa o primeiro e chama a próxima resposta
    regras[0]= f"int {regras[1]}; {regras[3]}"

def p_regra_id(regras):
  '''
  id : variavel
  '''
  #repassa o valor (palavra com ou sem numeros ) lido como uma id válida
  regras[0]=regras[1]
  

def p_error(regras):
  print("Erro de sintaxe"+ str(regras))
  
parser = yacc.yacc(debug=False) 

leitura= input(str("Digite o código:"))
resultado= parser.parse(leitura)

print(resultado)

