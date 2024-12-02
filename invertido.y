%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylineno;

/* Tabela de símbolos com suporte a escopo */
typedef struct simbolo {
    char* nome;
    int valor;
    struct simbolo* proximo;
} Simbolo;

Simbolo* tabela_simbolos = NULL;

int obter_valor(char* nome) {
    Simbolo* atual = tabela_simbolos;
    while (atual != NULL) {
        if (strcmp(atual->nome, nome) == 0) {
            return atual->valor;
        }
        atual = atual->proximo;
    }
    printf("Variavel '%s' nao definida. Usando valor 0.\n", nome);
    return 0;
}

void definir_variavel(char* nome, int valor) {
    Simbolo* atual = tabela_simbolos;
    while (atual != NULL) {
        if (strcmp(atual->nome, nome) == 0) {
            atual->valor = valor;
            return;
        }
        atual = atual->proximo;
    }
    Simbolo* novo = (Simbolo*)malloc(sizeof(Simbolo));
    novo->nome = strdup(nome);
    novo->valor = valor;
    novo->proximo = tabela_simbolos;
    tabela_simbolos = novo;
}

void yyerror(const char *s);
int yylex(void);

%}

%define parse.error verbose

%union {
    int intval;
    float floatval;
    char charval;
    char *strval;
}

%token <strval> ID
%token <intval> NUM
%token <floatval> FLOAT_NUM
%token <charval> CHAR_LITERAL
%token IF ELSE WHILE FOR INT FLOAT CHAR VOID RETURN PRINTF
%token EQ NE LE GE AND OR NOT
%token <strval> STRING

%type <intval> expressao
%type <intval> retorno_opt

%left OR
%left AND
%right NOT
%left EQ NE '<' '>' LE GE
%left '+' '-'
%left '*' '/'

%%

programa:
    lista_declaracoes { printf("Parsing concluido com sucesso.\n"); }
    ;

lista_declaracoes:
      /* vazio */
    | lista_declaracoes declaracao
    ;

declaracao:
      declaracao_variavel
    | declaracao_funcao
    | declaracao_controle
    | declaracao_expressao
    ;

declaracao_variavel:
    tipo ID ';' {
        definir_variavel($2, 0);
        printf("Variavel %s declarada com valor 0\n", $2);
    }
    | tipo ID '=' expressao ';' {
        definir_variavel($2, $4);
        printf("Variavel %s declarada com valor %d\n", $2, $4);
    }
    ;

tipo:
      INT
    | FLOAT
    | CHAR
    | VOID
    ;

declaracao_funcao:
    tipo ID '(' parametros ')' bloco_funcao
    ;

parametros:
      /* vazio */
    | lista_parametros
    ;

lista_parametros:
    parametro
    | lista_parametros ',' parametro
    ;

parametro:
    tipo ID
    ;

bloco_funcao:
    '{' lista_declaracoes retorno_opt '}'
    ;

retorno_opt:
      /* vazio */
    | RETURN expressao ';' {
        printf("Return com valor: %d\n", $2);
    }
    ;

bloco:
    '{' lista_declaracoes '}'
    ;

declaracao_controle:
      declaracao_fi
    | declaracao_elihw
    | declaracao_rof
    ;

declaracao_fi:
    IF '(' expressao ')' bloco
    | IF '(' expressao ')' bloco ELSE bloco
    ;

declaracao_elihw:
    WHILE '(' expressao ')' bloco
    ;

declaracao_rof:
    FOR '(' declaracao_expressao declaracao_expressao expressao ')' bloco
    ;

declaracao_expressao:
      expressao ';'
    | PRINTF '(' STRING lista_argumentos ')' ';' {
        printf("%s", $3);
    }
    | ID '=' expressao ';' {
        definir_variavel($1, $3);
        printf("Assigned %s = %d\n", $1, $3);
    }
    ;

lista_argumentos:
      /* vazio */
    | ',' expressao lista_argumentos
    ;

expressao:
      expressao '+' expressao { $$ = $1 + $3; }
    | expressao '-' expressao { $$ = $1 - $3; }
    | expressao '*' expressao { $$ = $1 * $3; }
    | expressao '/' expressao { $$ = $1 / $3; }
    | expressao EQ expressao { $$ = ($1 == $3); }
    | expressao NE expressao { $$ = ($1 != $3); }
    | expressao LE expressao { $$ = ($1 <= $3); }
    | expressao GE expressao { $$ = ($1 >= $3); }
    | expressao '<' expressao { $$ = ($1 < $3); }
    | expressao '>' expressao { $$ = ($1 > $3); }
    | expressao AND expressao { $$ = $1 && $3; }
    | expressao OR expressao { $$ = $1 || $3; }
    | NOT expressao { $$ = !$2; }
    | '(' expressao ')' { $$ = $2; }
    | NUM { $$ = $1; }
    | ID { $$ = obter_valor($1); }
    | chamada_funcao
    ;

chamada_funcao:
    ID '(' lista_argumentos_chamada ')'
    { 
        printf("Chamada de função %s\n", $1);
    }
    ;

lista_argumentos_chamada:
      /* vazio */
    | lista_argumentos_chamada_aux
    ;

lista_argumentos_chamada_aux:
    expressao
    | lista_argumentos_chamada_aux ',' expressao
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s na linha %d\n", s, yylineno);
}

int main() {
    return yyparse();
}
