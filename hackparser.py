################################################
#Parser module for TECS Assembler (Chapter 6).
################################################

import ply.lex as lex
from symbol_table import SymbolTable
from code import translate


tokens = (
        'A_COMMAND',
	'C_COMMAND',
	'L_COMMAND'
	)
#
#Token definitions
#

t_A_COMMAND = r'@[0-9]+|@[A-Za-z_]+'
t_C_COMMAND = r'[AMDJGTEQLNP01=\+\-\;]+'
t_L_COMMAND = r'\([A-Z\_\.\$\:]+\)'
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
asm = input('Name of .asm file: ')
prog = open(asm,'r')
assembly = prog.read()
prog.close()


#
#Build the lexer, feed it the assembly program input
#
lexer = lex.lex()
lexer.input(assembly)

#
#Main functions
#


symbols = SymbolTable()

def first_pass():
    line_no = 0
    while True:
        token = lexer.token()
        if not token:
            break
        if token.type == 'L_COMMAND':
            symbols.add_entry(symbol(token.value), line_no)
        else:
            line_no += 1
            
        

def second_pass():
    token_list = []
    while True:
        token = lexer.token()
        if not token:
            break
        if token.type == 'A_COMMAND':
            if token.value[1] in '1234567890': 
                token_list.append([token.type, symbol(token.value)])
            else:
                if symbols.contains(symbol(token.value)) == True:
                    token_list.append([token.type, symbols.symbol_table[symbol(token.value)]])
                else:
                    symbols.add_entry(symbol(token.value), symbols.next_addr)
                    token_list.append([token.type, symbols.symbol_table[symbol(token.value)]])
        if token.type == 'C_COMMAND':
            token_list.append([token.type, comp(token.value), dest(token.value), jump(token.value)])
    return token_list

first_pass()

lexer.input(assembly)

hack = asm[0:-4] + '.hack'

hack = open(hack, 'wb')
for i in translate(second_pass()):
    hack.write(i + '\n')
hack.close()
print symbols.symbol_table
