### INF1022-Analisadores-Lexicos
 Construção de um Analisador Léxico e Sintático, Trabalho Final de INF1022
 
## Projeto
O analisador léxico e sintático definido para a construção de um compilador de linguagem “Provol-One” foi desenvolvido com a biblioteca PLY que ultiliza uma leitura de parser ascendente LALR(1), que constrói um código executável na linguagem C. Para a testagem foi utilizado a execução por meio do terminal “python -m analisador” e em seguida o código solicita um “texto” para ser lido, que deve ser interpretado como linguagem Provol-One. 
Ao receber a entrada inserida, ele retorna um código C do que foi escrito em Provol-One, em caso de erro, o sistema imprime o último caracter que atrapalhou a leitura e o processamento do código é interrompido via o uso da função da biblioteca sys, a exit().  

## Gramática

- S' -> regra
- regra -> INICIO varlist MONITOR monitorar EXECUTE cmds TERMINO
- cmds -> cmd
- cmds -> cmd cmds
- cmd -> variavel IGUAL numero
- cmd -> variavel IGUAL variavel
- cmd -> funcao
- cmd -> IF condicao THEN cmds FIM
- cmd -> IF condicao THEN cmds ELSE cmds FIM
- cmd -> ENQUANTO condicao FACA cmds FIM
- cmd -> EVAL ABRE variavel VIRGULA variavel VIRGULA cmds FECHA
- cmd -> EVAL ABRE numero VIRGULA numero VIRGULA cmds FECHA
- funcao -> SOMA ABRE variavel VIRGULA variavel VIRGULA variavel FECHA
- funcao -> SOMA ABRE variavel VIRGULA numero VIRGULA variavel FECHA
- funcao -> SOMA ABRE numero VIRGULA variavel VIRGULA variavel FECHA
- funcao -> SOMA ABRE numero VIRGULA numero VIRGULA variavel FECHA
- funcao -> MULT ABRE numero VIRGULA numero VIRGULA variavel FECHA
- funcao -> MULT ABRE variavel VIRGULA variavel VIRGULA variavel FECHA
- funcao -> MULT ABRE variavel VIRGULA numero VIRGULA variavel FECHA
- funcao -> MULT ABRE numero VIRGULA variavel VIRGULA variavel FECHA
- funcao -> ZERO ABRE variavel FECHA
- condicao -> numero MAIOR variavel
- condicao -> numero MENOR variavel
- condicao -> numero IGUAL IGUAL variavel
- condicao -> variavel IGUAL IGUAL variavel
- condicao -> variavel IGUAL IGUAL numero
- condicao -> variavel MAIOR variavel
- condicao -> variavel MENOR variavel
- condicao -> variavel MAIOR numero
- condicao -> variavel MENOR numero
- condicao -> variavel
- monitorar -> variavel
- monitorar -> variavel VIRGULA monitorar
- varlist -> variavel

# Tokens Definidos

Os tokens definidos se encontram no arquivo analisador.py, e se tratam das palavras reservadas para denotar alguma operação descrita pela Provol-One.

- Operação: `IGUAL`, `SOMA`, `MULT`,`ZERO`

- Booleanos: `MAIOR`, `MENOR`, `IGUAL`

- Condicionais: `IF`, `THEN`, `ELSE`

- Loop: `ENQUANTO`, `EVAL`

- Fluxo: `INICIO`, `MONITOR`, `EXECUTE`, `TERMINO`, `FACA`,`FIM`

- Variaveis: `variavel`, `numero`, `monitorar`

- Outros tokens: `ABRE`, `FECHA`, `VÍRGULA`

Qualquer palavra utilizada que não faça parte da lista de tokens é categorizada como um erro, imprimindo uma mensagem de caracter ilegal. Quebras de linhas e parágrafos são ignorados.

# Análise sintática (YACC)

O parser lê a entrada vinda de um texto guardado no arquivo “codigo.txt” numa variável ‘leitura’.
Cada palavra é interpretada como 1 token e possui um índice, em ordem, na lista ‘regras’, e o
resultado da tradução é guardada no índice 0 desta lista. Para cada token não-terminal definido
nas funções, entre “‘...’”’, para as regras abaixo, a lista inicial é ‘ramificada’ e é chamada a
função de resolução daquele token não-terminal.

`p_regra_INICIO(regras)`: regra inicial da análise, determina as sessões principais que são
necessárias para iniciar o programa (por exemplo: quais variáveis devem ser inicializadas ao
início da aplicação, quais variáveis devem ser monitoradas, quais operações serão feitas, bem
como anunciar o encerramento da tradução)

`p_regra_cmds(regras)`: cmds é o token não terminal que permite que sejam utilizados de um a
diversos comandos ao longo da aplicação.

`p_regra_cmd(regras)`: cmd é o token que representa uma operação individual das possíveis
listadas acima (condicionais, loops, funções e definição de variáveis). Nela, se traduz
diretamente para o código C tais estruturas.

`p_regra_funcao(regras)`: define a tradução em C para operações aritméticas definidas segundo
a gramática de Provol-One (soma, mult ,zero).

`p_regra_condicao(regras)`: define a tradução em C para operações booleanas (maior, menor ou
comparação IGUAL) necessárias para construção de loops.

`p_regra_monitorar(regras)`: define a garantia de monitoramento de variáveis estabelecida nas
especificações da linguagem Provol-One, guardando a variáveis que serão monitoradas em
uma lista para aparecer com “Prints’s” em caso de alteração de valores na tradução em C.

`p_regra_varlist(regras)`: regras é o token não terminal que permite a inicialização de uma ou
mais regras, embora não seja estritamente necessário

`chamar_p_error(token_value)`: realiza uma chamada de erro no sistema e trava o
funcionamento utilizando a função sys.exit() do Python

`p_error(regras)`: função de erro necessária para biblioteca PLY que serve para notificar qual
erro de regra de sintaxe ocorreu

# Particularidades da nossa implementação

1. Função SOMA
	A implementação da função de SOMA neste trabalho se dá da seguinte forma:
	SOMA(A,B,C) onde A, B, e C são os argumentos da função
	A e B devem ser variáveis obrigatoriamente inicializadas com valores ou simplesmente números, enquanto que a variável C pode ou não ter sido inicializada anteriormente. Caso C não tenha sido inicializada, ela é inicializada neste momento. C é a variável em que o resultado da soma será armazenado.

2. Função MULT
A implementação da função de MULT neste trabalho se dá da seguinte forma:
	MULT(A,B,C) onde A, B, e C são os argumentos da função
	A e B devem ser variáveis obrigatoriamente inicializadas com valores ou simplesmente números, enquanto que a variável C pode ou não ter sido inicializada anteriormente. Caso C não tenha sido inicializada, ela é inicializada neste momento. C é a variável em que o resultado da soma será armazenado

3. Função EVAL
	Neste trabalho, EVAL não é uma função com retorno. Portanto, algumas utilizações desta função se tornam ilegais, como, por exemplo, Z = EVAL. A função funciona tanto com parâmetros de variável com variável quanto com número e número (onde ele cria um delta para rodar n vezes sendo esse n a diferença entre os dois números)

4. Inicialização
	Não é possível inicializar variáveis simultaneamente em condições IF e ELSE (a variável é inicializada apenas no bloco do IF, o que não garante a compilação correta do código), portanto, quaisquer variáveis utilizadas em IF e ELSE devem ter sido inicializadas com valores anteriormente à sua chamada em se forem usadas em ambas estruturas condicionais.

5. Listas Globais
Duas listas foram utilizadas para o gerenciamento da tradução correta em C, uma para as variáveis que vem em seguida do token MONITORA, que são guardadas na lista ‘monitorar’ e quando aparecem adicionam uma linha de ‘printf’ na tradução. A outra lista é a ‘inicializados’.

6. Condições
Na tarefa foi proposto apenas a condição if (variavel), porém expandimos para frases booleanas utilizando ‘>’ , ‘<’ e ‘==’.

# Testes

# Testes

## Tabela de Testes

| Código em Provol-One | Código em C |
| -------------------- | ----------- |
| ```INICIO a, b, c MONITOR a, b EXECUTE a = 5 b = 10 SOMA(a, b, c) TERMINO``` | ```#include <stdio.h> int main(void) { int a; int b; int c; a = 5; printf("%d", a); b = 10; printf("%d", b); c = a + b; return 0; }``` |
| `INICIO x, y, z MONITOR x, y EXECUTE x = 15 y = 20 IF x > y THEN z = x ELSE z = y FIM TERMINO` | `#include <stdio.h> int main(void) { int x; int y; int z; x = 15; printf("%d", x); y = 20; printf("%d", y); if (x > y) { z = x; } else{ z = y; } return 0; }` |
| `INICIO a, b, c, resultado MONITOR a, b, resultado EXECUTE a = 10 b = 20 SOMA(a, b, c) IF a < b THEN IF c MAIOR b THEN MULT(a, b, resultado) ELSE SOMA(a, b, resultado) FIM ELSE resultado = a FIM TERMINO` | `#include <stdio.h> int main(void) { int a; int b; int c; int resultado; a = 10; printf("%d", a); b = 20; printf("%d", b); c = a + b; if (a < b) { if (c > b) { resultado = a * b; printf("%d", resultado); } else { resultado = a + b; printf("%d", resultado); } } else { resultado = a; printf("%d", resultado); } return 0; }` |
| `INICIO i, j, sum, product, result MONITOR i, j, sum, result EXECUTE i = 1 j = 1 sum = 0 product = 1 result = 0 ENQUANTO i < 5 FACA j = 1 ENQUANTO j < 5 FACA MULT(i, j, product) SOMA(sum, product, sum) IF product > 10 THEN SOMA(result, sum, result) ELSE SOMA(result, 1, result) FIM SOMA(j, 1, j) FIM SOMA(i, 1, i) FIM TERMINO` | `#include <stdio.h> int main(void) { int i; int j; int sum; int product; int result; i = 1; printf("%d", i); j = 1; printf("%d", j); sum = 0; printf("%d", sum); product = 1; result = 0; printf("%d", result); while(i < 5) { j = 1; printf("%d", j); while(j < 5) { product = i * j; sum = sum + product; printf("%d", sum); if (product > 10) { result = result + sum; printf("%d", result); } else { result = result + 1; printf("%d", result); } j = j + 1; printf("%d", j); } i = i + 1; printf("%d", i); } return 0; }` |

