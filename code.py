########################################################################
#Code module for TECS Assembler (Chapter 6).
#Takes parsed assembly code and translates to machine code instructions.
########################################################################
from hackparser import token_list

#hash table mapping assembly dest mnemonic to machine instruction bits
dest_dict = {'null':'000', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 
    'AM':'101', 'AD':'110', 'AMD':'111'
	}

#hash table mapping assembly jump mnemonic to machine instruction bits
jump_dict = {'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 
    'JNE':'101', 'JLE':'110', 'JMP':'111'
	}
	
#hash table mapping assembly comp mnemonic to machine instruction bits
comp_dict = {'0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100', 'A':'0110000',
    '!D':'0001101', '!A':'0110001', '-D':'0001111', '-A':'0110011', 'D+1':'0011111',
	'A+1':'0110111', 'D-1':'0001110', 'A-1':'0110010', 'D+A':'0000010', 'D-A':'0010011',
	'A-D':'0000111', 'D&A':'0000000', 'D|A':'0010101', 'M':'1110000', '!M':'1110001', 
	'M+1':'1110111', 'M-1':'11110010', 'D+M':'1000010', 'D-M':'1010011', 'M-D':'1000111',
	'D&M':'1000000', 'D|M':'1010101'
	}

#translates A COMMAND into machine instruction
def a_code(token):
    token_binary = bin(int(token[1]))[2:]
    leading_zeros = 15 - len(token_binary)
    return '0' + '0' * leading_zeros + str(token_binary)


#transates C COMMAND into machine instruction
def c_code(token):
    comp = comp_dict[token[1]]
    dest = dest_dict[token[2]]
    jump = jump_dict[token[3]]
    return '111' + comp + dest + jump
	
#main loop -  creates list of individual machine instructions
machine_list = []

def translate(token_list):
    for token in token_list:
        if token[0] == 'A_COMMAND':
            machine_list.append(a_code(token))
        elif token[0] == 'C_COMMAND':
            machine_list.append(c_code(token))
    return machine_list
			
print translate(token_list)
