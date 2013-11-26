################################################
#Parser module for TECS Assembler (Chapter 6).
################################################

import ply.lex as lex
import symboltable
import code


tokens = (
        'A_COMMAND',
	'C_COMMAND',
	'L_COMMAND'
	)
#
#Token definitions
#

t_A_COMMAND = r'@[0-9]+|@[A-Za-z\.\$\_\:]+[A-Za-z0-9\.\$\_\:]+'
t_C_COMMAND = r'[AMDJGTEQLNP01=\+\-\;\!\&\|]+'
t_L_COMMAND = r'\([A-Za-z\.\$\_\:]+[A-Za-z0-9\.\$\_\:]+\)'
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
	


#Main functions

def first_pass():
    line_no = 0
    while True:
        token = lexer.token()
        if not token:
            break
        if token.type == 'L_COMMAND':
            table.add_entry(symbol(token.value), line_no)
        else:
            line_no += 1
            
        

def second_pass():
    token_list = []
    line_no = 0
    while True:
        token = lexer.token()
        if not token:
            break
        if token.type == 'A_COMMAND':
            if token.value[1] in '1234567890': 
                token_list.append([token.type, symbol(token.value)])
            else:
                if table.contains(symbol(token.value)) == True:
                    token_list.append([token.type, table.symbol_table[symbol(token.value)]])
                else:
                    table.add_entry(symbol(token.value), table.next_addr)
                    table.next_addr += 1
                    token_list.append([token.type, table.symbol_table[symbol(token.value)]])
        if token.type == 'C_COMMAND':
            token_list.append([token.type, comp(token.value), dest(token.value), jump(token.value)])
    return token_list



#Get the input from the .asm file
asm = input('Name of .asm file: ')
prog = open(asm,'r')
assembly = prog.read()
prog.close()


#Build the lexer, feed it the assembly program input for first pass
lexer = lex.lex()
lexer.input(assembly)

#Instantiate the symbol table
table = symboltable.SymbolTable()

#Parse the label commands
first_pass()

#Feed the assembly program input for the second pass
lexer.input(assembly)

#Open the output .hack file
hack = asm[0:-4] + '.hack'
hack = open(hack, 'wb')

#Parse the C and A COMMANDS, tranlate and write to .hack file
for i in code.translate(second_pass()):
    hack.write(i + '\n')
hack.close()

