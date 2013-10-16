Hack_Assembler
==============

Assembler for Hack machine I am currently building for Shimon Schoken and Noam Nisan's "The Elements of Computing Systems"
course. The assembler takes an assembly (.asm) file written in the Hack assembly language, parses it and translates it 
into machine code for the underlying hardware platform built earlier in the course.
 

There are three modules. hackparser.py contains the lexer written with ply, additional parsing functions and the main functions which use the 
code translation and memory addressing hash tables in code.py and symbol_table.py.

**Disclaimer -  I am not a programmer or computer scientist by trade. I'm simply building this as a learning experience.
                Therefore my code may not be the best. 
