%{
#include "invertido.tab.h"  // Garante que o Flex e o Bison compartilhem os mesmos tokens
%}

%%
"fi"            { return IF; }
"esle"          { return ELSE; }
"elihw"         { return WHILE; }
"rof"           { return FOR; }
"tni"           { return INT; }
"taolf"         { return FLOAT; }
"rahc"          { return CHAR; }
"diov"          { return VOID; }
"nruter"        { return RETURN; }
"ftnirp"        { return PRINTF; }
"dna"            { return AND; }
"ro"          { return OR; }
"ton"             { return NOT; }
"=="            { return EQ; }
"!="            { return NE; }
"<="            { return LE; }
">="            { return GE; }
\"([^\\\"]|\\.)*\"    {
    yylval.strval = strdup(yytext + 1);
    yylval.strval[strlen(yylval.strval) - 1] = '\0';
    return STRING;
}
[0-9]+\.[0-9]+ { yylval.floatval = atof(yytext); return FLOAT_NUM; }
[0-9]+          { yylval.intval = atoi(yytext); return NUM; }
\'[^\']\'       { yylval.charval = yytext[1]; return CHAR_LITERAL; }
[a-zA-Z_][a-zA-Z0-9_]* {
    yylval.strval = strdup(yytext);
    return ID;
}
"<"             { return '<'; }
">"             { return '>'; }
"+"             { return '+'; }
"-"             { return '-'; }
"*"             { return '*'; }
"/"             { return '/'; }
"="             { return '='; }
";"             { return ';'; }
","             { return ','; }
"("             { return '('; }
")"             { return ')'; }
"{"             { return '{'; }
"}"             { return '}'; }
[ \t]+          { /* Ignorar espaços em branco */ }
\n              { /* Incrementa o número da linha automaticamente */ }
.               { printf("Caractere nao reconhecido: %s na linha %d\n", yytext, yylineno); }

%%

int yywrap(void) {
    return 1;
}
