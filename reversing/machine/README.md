SIMPLEMACHINE
A SIMPLE MACHINE
WHAT IS THIS?
You stand before assembly code for a custom Virtual Machine.

You will find the flag once you understand the code.

Everything you need to know is described below. Don?t forget to check ou the example code!

Get the machine code Here

TOP LEVEL DESCRIPTION
The machine is stack based, which means most operations pop data off the top of the stack and push the result. for further reference, https://en.wikipedia.org/wiki/Stack_machine#Advantages_of_stack_machine_instruction_sets

The machine state is defined by an Instruction Pointer, and a Stack data structure.

The next instruction to be executed is pointed to by IP, and it generally reads/write values from/to the top of the stack.

Every opcode is exactly 1 byte in size. The program is read and executed sequentially starting at offset 0 in the file.

Execution stops if an invalid stack address is referenced or the IP is out of code bounds.

INSTRUCTION SET
IMPORTANT!
IP is incremented as the instruction is read (before decode/execute).

This increment is not mentioned in the instruction pseudo-code. Therefore, every instruction that adds an offset to IP will result in IP = IP + offset + 1.

An instruction that resets IP as IP = new_value discards the increment.

INSTRUCTION PSEUDO CODE NOTATIONS
stack.push([value]) - pushes the value to the stack

stack.pop() - dequeue the last value pushed to the stack .

a = stack.pop() - dequeue the last value pushed to the stack, save value to pseudo-variable ?a?.

stack.empty() - true if there are no more values on the stack, false otherwise

stack[N] - the value of the Nth element on the stack

IP - the instruction pointer.

STACK INSTRUCTIONS:
Push <value>

opcode is 0x80 + value
Pushes the value to the stack, stack[0] is now , stack[1] is now the previous stack[0] value, and so on.
value <= 0x7f
Push 0x32 is encoded as 0xB2.
stack.push(value)


Load <offset>

opcode is 0x40 + offset
Pushes the value at stack[offset] to the stack.
value <= 0x3f
Load 0x12 is encoded as 0x52.
Loading from an offset out of bounds (i.e pushing 10 values and loading from offset 12) will cause a fault and execution will terminate.
stack.push(stack[offset])
Pop

opcode 0x20
Same encoding as Swap 0
Swap 0 is an empty statement, thus this opcode pops a value from the stack without doing anything with it.
stack.pop()
Swap <index>

opcode is 0x20 + index
Swaps the element at HEAD with the element at index.
1 <= index < 0x20.
Swap 3 is encoded as 0x23.
temp = stack[index]
stack[index] = stack.pop()
stack.push(temp)


ARITHMETIC INSTRUCTIONS
These instructions read 2 values off the stack and push the result. ### Single outupt instructions:

Add

opcode is 0x00.
operands are viewed as signed bytes
stack.push(stack.pop() + stack.pop())
Subtract

opcode is 0x01.
operands are viewed as signed bytes
stack.push(stack.pop() - stack.pop())
Multiply

opcode is 0x03.
operands are viewed as signed bytes
stack.push(stack.pop() * stack.pop())
2-BYTE OUTPUT
Divide

opcode is 0x02.
division reminder is at HEAD, division result follows
operands are viewed as unsigned bytes
a = stack.pop()
b = stack.pop()
stack.push(a / b)
stack.push(a % b)
FLOW CONTROL INSTRUCTIONS:
These instructions change the Instruction Pointer and allow for loops, function calls, etc.

Jump

opcode is 0x10. Jumps to offset stack[0].
offset is signed! Jumping to a negative offset is a jump backwards.
Pops an offset from the stack, adds it to IP.
IP = IP + stack.pop()


Call

opcode is 0x11. Jumps to stack[0], saves origin.
same as Jump, only IP before execution is pushed.
offset is signed! Calling to a negative offset is a jump backwards.
offset = stack.pop()
stack.push(IP) ; note that IP was already incremented here, points to next instruction.
IP = IP + offset
Ret

opcode is 0x12. Pops value from the stack, moves IP to the popped value.
IP = stack.pop()
CJE

opcode is 0x14. Jumps to stack[0] if stack[1] == stack[2]. pops all values either way.
offset is signed! Jumping to a negative offset is a jump backwards.
offset = stack.pop()
if stack.pop() == stack.pop():
    IP = IP + offset
JSE

opcode is 0x18. Adds stack[0] to IP if it is the last value on the stack.
offset = stack.pop()
if stack.empty():
    IP = IP + offset
INPUT OUTPUT INSTRUCTIONS:
These instructions either output an ASCII byte or read an ASCII byte from the input/output device.

Read

opcode is 0x08
Waits for a single byte to be read from the input, pushes the byte to the top of the stack.
stack.push(read(stdin))
Write

opcode is 0x09
outputs the top of the stack as ASCII.
write(stdout, stack.pop())
LET?S RUN TOGEATHER
Here you?ll find an execution log of a simple program.

Note that the ?;? symbol starts a comment line

lines of the form ?; >| value1 value2 value3? show the stack state before the following instruction. The stack head is to the left (the first value after >| is SP[0])

The stack state inside the called function is a direct continuation of the caller execution

Note that ?Word:? defines a label, which basically names a line of code.

;>|
    Push 2
;>| 02
    Push 7F
;>| 7F 02
    Read            ; assuming user inputs 0x3
;>| 03 7F 02
    Push 0A         ; OFFSET of Adder
;>| 0A 03 7F 02
    Call
;>| 82 02
    Divide
;>| 00 41
    Swap 1
;>| 41 00
    Write
;>| 00
    Pop
;>|
    Push 0C         ; OFFSET of More
;>| 0C
    JSE
;>| 

NotReached:
    Push 4
    Push 0
    Sub     ; constructs offset of NotReached, which is -4 (0xFC)
    Call

Adder:
;>| 05 03 7F 02
    Load 2
;>| 7F 05 03 7F 02
    Load 2
;>| 03 7F 05 03 7F 02
    Add
;>| 82 05 03 7F 02
    Swap 3
;>| 7F 05 03 82 02
    Pop
;>| 05 03 82 02
    Swap 1
;>| 03 05 82 02
    Pop
;>| 05 82 02
    Ret
;>| 82 02


More:
; fill the rest on your own!
;>| 
    Push 44
;>| 
    Push 4E
;>| 
    Push 45
;>| 
    Push 20
;>| 
    Write
;>| 
    Write
;>|    
    Write
;>|     
    Write

; Program ends here
On the displayed run, The program printed ?A END?

Your job is to decipher the code and give us the flag.

Good Luck!

