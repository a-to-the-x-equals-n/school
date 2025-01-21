%option header-file = "lex.yy.h"
%option noyywrap
%{
#include "parser.tab.h"
#include <stdlib.h>
%}

%% 

[0-9]+                          { yylval.i = atoi(yytext); return INT;}
0[0-7]+                         { yylval.i = strtol(yytext, NULL, 8); return INT; } 
0[xX][0-9a-fA-F]+               { yylval.i = strtol(yytext, NULL, 16); return INT; } 
[0-9]*"."[0-9]+                 { yylval.i = atoi(yytext); return FLOAT; }

e[0-9]+                         { return EXPO;}
[+]                             { return ADD; }
[-]                             { return MINUS; }
[/]                             { return DIV; }
[*]                             { return MUL; }
[%]                             { return MOD; }
[=]                             { return EQ; }
 
[a-fA-F]                        { yylval.ch = yytext[0]; return ID; }
 
[(]                             { return OP; }
[)]                             { return CP; }
[ \t\r]                         {/* Do Nothing */}
[\n]                            { return yytext[0]; }
.                               { return INVALID; }

%%