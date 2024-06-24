### INF1022-Analisadores-Lexicos
 Construção de um Analisador Léxico e Sintático, Trabalho Final de INF1022
 
## Projeto
O analisador léxico e sintático definido para a construção de um compilador de linguagem “Provol-One” foi desenvolvido com a biblioteca PLY que ultiliza uma leitura de parser ascendente LALR(1), que constrói um código executável na linguagem C. Para a testagem foi utilizado a execução por meio do terminal “python -m analisador” e em seguida o código solicita um “texto” para ser lido, que deve ser interpretado como linguagem Provol-One. 
Ao receber a entrada inserida, ele retorna um código C do que foi escrito em Provol-One, em caso de erro, o sistema imprime o último caracter que atrapalhou a leitura e o processamento do código é interrompido via o uso da função da biblioteca sys, a exit().  

## Gramática
Seguindo as os requisitos de estrutura do trabalho, a gramática aceita a construção inicial sendo um aviso de inicio uma lista de variáveis, uma declaração de monitoramento com outra lista de variáveis, um token para aviso de inicio de comandos e operações e por fim, um token de termino de leitura.
Dentro disso, algumas estruturas também tiveram que ser contempladas como a criação de loops feitos pelo (while em C) que são acionados a partir do token ‘ENQUANTO’ e também por meio da função EVAL que cria um for. 
Além destas as operações de soma, multiplicação e redefinição dos valores também são contempladas, sendo as duas primeiras escritas em Provol-One como se fosse uma função, porém são compiladas em C apenas como operações matemática diretas. Para terminar, também foram criadas maneiras de ler condicionais por estruturas de IF-THEN ou IF-THEN-ELSE, que são replicadas na mesma lógica da linguagem C.
Rule 0     S' -> regra
Rule 1     regra -> INICIO varlist MONITOR monitorar EXECUTE cmds TERMINO
Rule 2     cmds -> cmd
Rule 3     cmds -> cmd cmds
Rule 4     cmd -> id IGUAL numero
Rule 5     cmd -> id IGUAL id
Rule 6     cmd -> funcao
Rule 7     cmd -> IF condicao THEN cmd
Rule 8     cmd -> ELSE cmd
Rule 9     cmd -> ENQUANTO condicao FACA cmds FIM
Rule 10    cmd -> EVAL ABRE id VIRGULA id VIRGULA cmds FECHA
Rule 11    cmd -> EVAL ABRE numero VIRGULA numero VIRGULA cmds FECHA
Rule 12    funcao -> SOMA ABRE id VIRGULA id FECHA
Rule 13    funcao -> SOMA ABRE id VIRGULA numero FECHA
Rule 14    funcao -> MULT ABRE id VIRGULA id FECHA
Rule 15    funcao -> MULT ABRE id VIRGULA numero FECHA
Rule 16    funcao -> id IGUAL MULT ABRE id VIRGULA
Rule 17    funcao -> ZERO ABRE id FECHA
Rule 18    condicao -> numero MAIOR id
Rule 19    condicao -> numero MENOR id
Rule 20    condicao -> numero IGUAL IGUAL id
Rule 21    condicao -> id IGUAL IGUAL id
Rule 22    condicao -> id IGUAL IGUAL numero
Rule 23    condicao -> id MAIOR id
Rule 24    condicao -> id MENOR id
Rule 25    condicao -> id MAIOR numero
Rule 26    condicao -> id MENOR numero
Rule 27    condicao -> id
Rule 28    monitorar -> id
Rule 29    monitorar -> id VIRGULA monitorar
Rule 30    varlist -> id
Rule 31    varlist -> id VIRGULA varlist
Rule 32    id -> variavel

# Observações
Para auxiliar na lógica e para cumprir alguns requisitos foi necessário expandir a sintaxe delimitada no trabalho para conseguir fazer a leitura de todas as frases possíveis. Foi necessário criar o token não terminal “monitorar” como forma de diferenciar de um varlist qualquer, pois o varlist escreve a inicialização de uma variável no sistema enquanto o monitorar só fica guardando no processamento do código que toda vez que aparecer, é necessário um “printf”. 
Por questões de organização e redução de conflito de regras os tokens não terminais “funcao” e “condicao” também foram criados, dessa forma, o agrupamento de leituras e regras ficou mais claro para execução além de permitir explorar algumas possibilidades além dos requisitos mínimos, como maneiras possíveis de fazer uma operação com variáveis e formatos diferentes de escrever as condições a serem interpretadas pelo compilador.
