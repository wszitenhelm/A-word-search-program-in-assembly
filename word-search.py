@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@
@ ( from practical 6)
@ Print an integer on the screen , followed
@ by a newline . ( uses C library function )
@
@ arguments : r1 : integer to be printed
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@
.global printf
print_num :
push {r0-r3 , lr }
ldr r0 , =fmt
bl printf
pop {r0-r3 , lr }
bx lr
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@
@ ( from practical 6)
@ Read a string from the terminal .
@ ( only the first 1000000 characters are read )
@
@ arguments : r1 : address of string used to
@ store result
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@
read_str :
push {r0-r7 , lr}
@ read a string from the terminal
mov r0 , #0 @ 0 = std input ( terminal )
ldr r2 , =#1000000 @ max num of bytes to read
mov r7 , #3 @ 3 = " read " system call
svc #0 @ make the system call
pop {r0-r7 , lr}
bx lr
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ Compute the length of a zero terminated
@ string .
@
@ arguments : r1 - string address
@ results : r0 - length of string
str_length:
push {r1 , r2 , lr}
mov r0 , #0
str_length_loop :
ldrb r2 , [ r1 ] , #1
cmp r2 , #0
beq str_length_end
add r0 , #1
b str_length_loop
str_length_end:
pop {r1 , r2 , lr}
bx lr
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ Print the first n characters of a string
@
@ arguments : r1 - string address
@ r2 - num of characters
@ returns : ( nothing )
print_str_n :
push {r0-r7 , lr}
mov r0 , #1 @ r0 = output device = std output
@ r1 = string address
@ r2 = num of bytes
mov r7 , #4 @ r7 = sys call code (4 = "write ")
svc #0 @ print !
pop {r0-r7 , lr}
bx lr
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ Print a zero terminated string
@
@ arguments : r1 - string address
@ returns : ( nothing )
print_str :
push {r0-r2 , lr}
bl str_length
mov r2 , r0
bl print_str_n
pop {r0-r2 , lr}
bx lr
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ Print a newline character
@
@ arguments : ( nothing )
@ returns : ( nothing )
print_newline:
push {r1 , lr}
ldr r1 , =newline
bl print_str
pop {r1 , lr}
bx lr


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ This function returns 1 if the string in r1
@ is a prefix of the string in r2
@
@ arguments : r1 - prefix string address
@ r2 - string address
@ returns : r0 - 1 if r1 is a prefix of r2
@ 0 otherwise
starts_with:
push {r1-r6, lr}
bl str_length
mov r6, r0    @ in r6 there is a lenght of prefix string which address is in r1
mov r0, #0         
mov r4, #0
mov r5, #0
starts_with_loop:
ldrb r3, [r1], #1
ldrb r4, [r2], #1
cmp r3, r4
moveq r0, #1
bne finish
add r5, #1
cmp r5, r6
bne starts_with_loop
finish:
pop {r1-r6, lr}
bx lr 


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ Return the address of the end
@ of the currentline , or of the end of
@ the text
@
@ arguments : r1 - address of current location
@ in string
@ returns : r0 - address of the next newline
@ character , or of the end of the
@ string
find_eol :
push {r1, r2, lr}
mov r2, #0
mov r0, #0
find_eol_loop:
ldrb r2, [r1]
cmp r2, #10       @ checking if this is the end of line
moveq r0, r1
beq skip
cmp r2, #0        @ checking if this is the end of file
moveq r0, r1
beq skip
add r1, #1
b find_eol_loop
skip: 
pop {r1, r2, lr}
bx lr


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ Print the string from the location r1 to the
@ end of the line
@
@ arguments : r1 - string address
@ returns : ( nothing )
print_line:
push {r1-r3, lr}
mov r2, #0       @ r2 stores the lenght of the string
mov r3, #0
print_line_loop:
ldrb r3, [r1], #1
cmp r3, #10      @ checking if this is the end of line 
beq print_       
cmp r3, #0       @ checking if this is the end of file 
beq print_
addne r2, #1
bne print_line_loop
print_:
pop {r1}
bl print_str_n
pop {r2, r3, lr}
bx lr


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
.global main
main:
ldr r1 , =txt
bl read_str @ read the text from the terminal
@ and store it in the txt string
ldr r1 , =search_string
ldr r2 , =txt
mov r3 , #1 @ r3 = line number
mov r4 , r2 @ r4 = pos of start of curr line
mov r6 , #1 @ r6 = total num of lines in file
@ ( the file starts at line 1)
mov r7 , #0 @ r7 = num of lines that match

@ I added this register here to control if the line was printed 
mov r8, #0  @ r8 = last line that was printed

loop :
ldrb r5, [r2]
cmp r5, #10
addeq r6, #1
moveq r4, r2
addeq r4, #1
addeq r3, #1
cmp r5, #0
beq end_
bne check

@ checks if a search string is a prefix of string 
check :
bl starts_with
cmp r0, #1
beq if_printed
bne another

@ checks if that line has already been printed
if_printed :
cmp r8, r3
bne to_print
beq another

@ prints num of line, line itself and adds 1 to lines that match
to_print :
push {r1}
mov r8, r3       
add r7, #1
mov r1, r3
bl print_newline  
bl print_num
mov r1, r4
bl print_line
pop {r1}
b another

@ goes back to main loop to check another character 
another : 
add r2, #1
b loop

@ prints total num of lines and lines that matches 
end_ :
push {r1}
ldr r1, =num_of_lines_str
bl print_newline
bl print_str
mov r1, r6
bl print_num
ldr r1, =num_of_matches_str
bl print_str
mov r1, r7
bl print_num
pop {r1}

@@ @@
mov r7 , #1
svc #0
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
.data
search_string: .asciz "blue"
newline: .asciz "\n"
num_of_lines_str: .asciz "total num of lines : "
num_of_matches_str: .asciz "num of matches : "
fmt: .asciz "%d\n"
txt: .space 1000000 @ input text as a
                    @ single string
.end
