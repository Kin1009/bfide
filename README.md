# bfide
 A simple standalone-able brainfuck IDE
# What is brainfuck?
Brainfuck is an esoteric programming language created in 1993 by Urban Müller. Notable for its extreme minimalism, the language consists of only eight simple commands, a data pointer and an instruction pointer.
# Language
The language consists of eight commands. A brainfuck program is a sequence of these commands, possibly interspersed with other characters (which are ignored). The commands are executed sequentially, with some exceptions: an instruction pointer begins at the first command, and each command it points to is executed, after which it normally moves forward to the next command. The program terminates when the instruction pointer moves past the last command.
- The brainfuck language uses a simple machine model consisting of the program and instruction pointer, as well as a one-dimensional array of at least 30,000 byte cells (this program has infinite) initialized to zero; a movable data pointer (initialized to point to the leftmost byte of the array); and two streams of bytes for input and output (most often connected to a keyboard and a monitor respectively, and using the ASCII character encoding).
- The eight language commands each consist of a single character:

Character	Meaning

">"	Increment the data pointer by one (to point to the next cell to the right).

"<"	Decrement the data pointer by one (to point to the next cell to the left).

"+"	Increment the byte at the data pointer by one.

"-"	Decrement the byte at the data pointer by one.

"."	Output the byte at the data pointer.

","	Accept one byte of input, storing its value in the byte at the data pointer.

"["	If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching "]" command. (In this program, "[" mark as a jump for "]" so some programs (especially input programs) don't work)

"]"	If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.

"[" and ] match as parentheses usually do: each "[" matches exactly one "]" and vice versa, the "[ comes first, and there can be no unmatched "[" or "]" between the two.

# Built-in Brainfuck code generator algorithm
The generator here takes ord() of every character, then get the divisors of that number, take 1 / 2 middle divisors, then multiply them.

Code for multiplying:

">x[<y>-]<.[-]"

Where x is "+"*x, y is "+"*y

It is memory efficent (Use only 2 bytes for the whole program!) but that code don't work well with prime numbers (long code, still take 2 bytes of memory so don't worry).
# Examples
Hello, world!

">++++++++[<+++++++++>-]<.[-]>+[<+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>-]<.[-]>+++++++++[<++++++++++++>-]<.[-]>+++++++++[<++++++++++++>-]<.[-]>+++[<+++++++++++++++++++++++++++++++++++++>-]<.[-]>++++[<+++++++++++>-]<.[-]>++++[<++++++++>-]<.[-]>+++++++[<+++++++++++++++++>-]<.[-]>+++[<+++++++++++++++++++++++++++++++++++++>-]<.[-]>++++++[<+++++++++++++++++++>-]<.[-]>+++++++++[<++++++++++++>-]<.[-]>++++++++++[<++++++++++>-]<.[-]>+++[<+++++++++++>-]<.[-]"

Notepad

"+[>,.<]"