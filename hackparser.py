################################################
#Parser module for TECS Assembler (Chapter 6).
################################################

import ply.lex as lex

tokens = (
    'A_COMMAND',
	'C_COMMAND',
	'L_COMMAND'
	)
#
#Token definitions
#

t_A_COMMAND = r'@[0-9]+'
t_C_COMMAND = r'[M|D|A].+'
t_L_COMMAND = r'\([A-Z]+\)'
t_ignore = ' \t'

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
	
def t_comment(t):
    r'\/\/.*'
    t.lexer.skip(1)

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
	
	
#
#Functions for parsing token values
#

#retrieves decimal value assignment from an A COMMAND or label from a L COMMAND
def symbol(value):
    if '@' in value:
        return value[1:]
    else:
	    return value[1:-1]

#retrieves destination from a C COMMAND if one exists
def dest(value):
    if '=' in value:
        loc = value.find('=')
        return value[0:loc]
    return 'null'
	

#retrieves computation mnemonic from a C COMMAND
def comp(value):
	loceq = value.find('=')
	locsc = value.find(';')
	if '=' in value and ';' in value:
		return value[loceq+1:locsc]
	if '=' in value and ';' not in value:
	    return value[loceq+1:]
	if '=' not in value and ';' in value:
	    return value[0:locsc]

#retrieves jump mnemonic from a C COMMAND if one exists
def jump(value):
    if ';' in value:
        locsc = value.find(';')
        return value[locsc+1:]
    return 'null'
	
#
#Get the input file
#
prog = open('c:/users/troy/documents/github/hack_assembler/test.txt','r')
assembly = prog.read()
prog.close


#
#Build the lexer, feed it the assembly program input
#
lexer = lex.lex()
lexer.input(assembly)

#
#Main loop
#
	
token_list = []

while True:
    token = lexer.token()
    if not token:
	    break
    if token.type == 'A_COMMAND' or token.type == 'L_COMMAND':
	    token_list.append([token.type, symbol(token.value)])
    if token.type == 'C_COMMAND':
	    token_list.append([token.type, comp(token.value), dest(token.value), jump(token.value)])
		
		
print token_list
		
