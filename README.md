# MacroScript

Vídeo: https://youtu.be/AT6TMavilDQ


EBNF


```bash
PROGRAM = { DECLARATION } ;

DECLARATION = ( ASSIGNMENT | FUNCTION_CALL | COMMAND | CONDITIONAL | TRY_CATCH | EXPRESSION_STATEMENT ), ";" ;

ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;

FUNCTION_CALL = IDENTIFIER, "(", [ ARGUMENTS ], ")" ;

COMMAND = COMMAND_KEYWORD, [ ARGUMENTS ] ;

COMMAND_KEYWORD = "press" | "exit" | "show" | "tryagain" ;

CONDITIONAL = "if", "(", EXPRESSION, ")", BLOCK, [ "else", BLOCK ] ;

TRY_CATCH = "try", ":", BLOCK, [ "catch", ":", BLOCK ] ;

BLOCK = "{", { DECLARATION }, "}" ;

EXPRESSION_STATEMENT = EXPRESSION ;

EXPRESSION = COMPARISON ;

COMPARISON = ADDITION, { ( "==" | "<" | ">" ), ADDITION } ;

ADDITION = TERM, { ( "+" | "-" ), TERM } ;

TERM = FACTOR, { ( "*" | "/" ), FACTOR } ;

FACTOR = [ ( "+" | "-" ) ], ( NUMBER | STRING | IDENTIFIER | TECLA | "(", EXPRESSION, ")" ) ;

ARGUMENTS = ARGUMENT, { ",", ARGUMENT } ;

ARGUMENT = EXPRESSION | TECLA ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

NUMBER = DIGIT, { DIGIT } ;

STRING = '"', { CHARACTER }, '"' ;

TECLA = UPPERCASE_LETTER, { UPPERCASE_LETTER } ;

LETTER = LOWERCASE_LETTER | UPPERCASE_LETTER ;

LOWERCASE_LETTER = ( "a" | ... | "z" ) ;

UPPERCASE_LETTER = ( "A" | ... | "Z" ) ;

DIGIT = ( "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ) ;

CHARACTER = any character except '"' and control characters ;

```
