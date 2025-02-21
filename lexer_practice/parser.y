%{
#include <stdio.h>
#include <stdlib.h>

extern int yyerror(char *message);
extern int yylex(void);
%}

%union
{
    int i;
    char ch;
}

%token<i> INT FLOAT
%token<ch> ID

%token MINUS ADD OP CP MUL DIV MOD EQ EXPO INVALID

%type<i> e

%left MINUS ADD
%left MUL DIV MOD
%left OP CP
%left EXPO

%{
static int IDs[6];
%}

%%
program:
    program statement '\n'
|	program error '\n'		{ yyerrok; }
|   program INVALID         { printf("Invalid Syntax!");}
|	/* empty */
;

statement:
	e           { printf("%d\n", $1); }
|	ID EQ e	    { IDs[$1] = $3; printf("%c = %d\n", $1, $3);}

e   :   
    INT        
|   FLOAT          
|   ID          { $$ = IDs[$1];}
|   e ADD e     { $$ = $1 + $3; }
|   e MINUS e   { $$ = $1 - $3; }
|   e MOD e     { $$ = $1 % $3; }
|   e DIV e     { $$ = $1 / $3; }
|   e MUL e     { $$ = $1 * $3; }
|   e EXPO e    { $$ = $1 ^ $3; }
|   OP e CP     { $$ = $2; }
;

%%
