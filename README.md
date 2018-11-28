# Brasilex
Uma linguagem compilada de alta produtividade adequada a lingua brasileira e sintaxe similar a C

# Introdução
A ideia ao desenvolver esta lingaugem foi aproximar iniciantes em programação que falam portgues (e não são muito habituados ao ingles) a estabelecer um primeiro contato com a popular linguagem de programação C. O objetivo é fazer entender os componentes básicos sem a barreira da lingua estrangeira, para que, futuramente, este passo possa ser dado com maior tranquilidade, já conhecendo a estrutura geral da sintaxe da linguagem.

Ao mesmo tempo, o desenvolvimento desta linguagem se prova uma otima oportunidade de aprendizado sobre linguagens, gramaticas e a construção de um compilador, componentes estes estudados em sala de aula e aprofundados com o auxilio deste projeto.


# Recursos

1. Compilado;
2. sem tipagem forte nem declaração de variável;
3. Sintaxe extremamente parecida com C com mudança de alguns tokens para português;
4. 100% PT-BR;
5. Inclue loops, blocos condicionais e imprime variaveis;

## EBNF:

```ebnf
program = "vazio", "principal", "(", ")", commands;
commands = "{", {command}, "}" ;
command = assignment | print | if_else | while | commands;

assignment = identifier , "=" , (expression | scanf), ";";
print = "imprime" , "(", expression , ")", ";";
if_else = "se", "(", bool_exp, ")", commands, ["senao", commands];
while = "enquanto", "(", bool_exp, ")", commands;

bool_exp = bool_term, {"ou", bool_term}; 
bool_term = bool_factor, {"e", bool_factor};
bool_factor = rel_expr;
rel_expr = expression, {("<" | ">" | "=="), expression};
expression = term, { ("+" | "-"), term };
term = factor , { ("*" | "/"), factor };
factor = (("+" | "-") , factor) | num | ("(" , expression , ")") | identifier;

scanf = "scanf", "(", ")";
identifier = letter, { letter | digit | "_" };
num = digit, {digit};
letter = "a" .. "Z";
digit = "0" .. "9";
```

## Diagrama Sintatico:

![Alt text](imgs/brasilex_ds.png?raw=true "SYNTAX DIAGRAM")