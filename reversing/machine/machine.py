from abc import ABCMeta, abstractmethod
import sys
import string
import traceback


class Opcode(object):
    def __init__(self, name, value, instruction):
        self.name = name
        self.value = value
        self.instruction = instruction

    def __str__(self):
        return self.name

    def run(self, machine):
        self.instruction.run(machine=machine)


class ArgumentOpcode(Opcode):
    def __init__(self, name, base_value, instruction, argument):
        super(ArgumentOpcode, self).__init__(name, base_value+argument, instruction)
        self.argument = argument

    def run(self, machine):
        self.instruction.run(machine, self.argument)

    def __str__(self):
        return self.name + " " + hex(self.argument)


class Instruction(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, base_opcode):
        self.name = name
        self.base_opcode = base_opcode

    def __str__(self):
        return self.name

    def generate_opcodes(self):
        yield Opcode(self.name, self.base_opcode, self)


class ArgumentInstruction(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, base_opcode, argument_range):
        self.name = name
        self.base_opcode = base_opcode
        self.argument_range = argument_range

    @abstractmethod
    def run(self, machine, argument):
        raise NotImplementedError

    def generate_opcodes(self):
        min, max = self.argument_range[0], self.argument_range[1]

        for arg_value in xrange(min, max+1):
            yield ArgumentOpcode(self.name, self.base_opcode, self, arg_value)

    def __str__(self):
        return self.name


class PushInstruction(ArgumentInstruction):
    def __init__(self):
        super(PushInstruction, self).__init__("push",
                                              base_opcode=0x80,
                                              argument_range=(0, 0x7f))

    def run(self, machine, argument):
        machine.stack.push(argument)


class LoadInstruction(ArgumentInstruction):
    def __init__(self):
        super(LoadInstruction, self).__init__('load',
                                              base_opcode=0x40,
                                              argument_range=(0, 0x3f))

    def run(self, machine, argument):
        value = machine.stack[argument]
        machine.stack.push(value)


class PopInstruction(Instruction):
    def __init__(self):
        super(PopInstruction, self).__init__('pop', base_opcode=0x20)

    def run(self, machine):
        machine.stack.pop()


class SwapInstruction(ArgumentInstruction):
    def __init__(self):
        super(SwapInstruction, self).__init__('swap',
                                              base_opcode=0x20,
                                              argument_range=(1, 0x19))

    def run(self, machine, argument):
        machine.stack[argument], machine.stack[0] = machine.stack[0], machine.stack[argument]


class AddInstruction(Instruction):
    def __init__(self):
        super(AddInstruction, self).__init__('add', base_opcode=0)

    def run(self, machine):
        a = machine.stack.pop()
        b = machine.stack.pop()
        machine.stack.push((a+b) & 0xFF)


class SubInstruction(Instruction):
    def __init__(self):
        super(SubInstruction, self).__init__('sub', base_opcode=0x1)

    def run(self, machine):
        a = machine.stack.pop()
        b = machine.stack.pop()
        machine.stack.push((a - b) & 0xFF)


class MulInstruction(Instruction):
    def __init__(self):
        super(MulInstruction, self).__init__('mul', base_opcode=0x03)

    def run(self, machine):
        a = machine.stack.pop()
        b = machine.stack.pop()
        machine.stack.push((a*b) & 0xFF)


class DivInstruction(Instruction):
    def __init__(self):
        super(DivInstruction, self).__init__('div', base_opcode=0x02)

    def run(self, machine):
        a = machine.stack.pop()
        b = machine.stack.pop()
        machine.stack.push((a / b) & 0xFF)
        machine.stack.push((a % b) & 0xFF)


class JumpInstruction(Instruction):
    def __init__(self):
        super(JumpInstruction, self).__init__('jump', base_opcode=0x10)

    def run(self, machine):
        machine.ip = (machine.ip + machine.stack.pop()) & 0xFF


class CallInstruction(Instruction):
    def __init__(self):
        super(CallInstruction, self).__init__('call', base_opcode=0x11)

    def run(self, machine):
        offset = machine.stack.pop()
        machine.stack.push(machine.ip)
        machine.ip = (machine.ip + offset) & 0xFF


class RetInstruction(Instruction):
    def __init__(self):
        super(RetInstruction, self).__init__('ret', base_opcode=0x12)

    def run(self, machine):
        machine.ip = machine.stack.pop()


class JEInstruction(Instruction):
    def __init__(self):
        super(JEInstruction, self).__init__('je', base_opcode=0x14)

    def run(self, machine):
        offset = machine.stack.pop()
        a = machine.stack.pop()
        b = machine.stack.pop()

        if a == b:
            machine.ip = (machine.ip + offset) & 0xFF


class JSEInstruction(Instruction):
    def __init__(self):
        super(JSEInstruction, self).__init__('jse', base_opcode=0x18)

    def run(self, machine):
        offset = machine.stack.pop()

        if machine.stack.empty():
            machine.ip = (machine.ip + offset) & 0xFF


class ReadInstruction(Instruction):
    def __init__(self, input):
        super(ReadInstruction, self).__init__('read', base_opcode=0x08)
        self.input = input

    def run(self, machine):
        b = self.input.read(1)
        machine.stack.push(b)


class WriteInstruction(Instruction):
    def __init__(self, output):
        super(WriteInstruction, self).__init__('write', base_opcode=0x09)
        self.output = output

    def run(self, machine):
        b = machine.stack.pop()
        self.output.write(b)


class InstructionSet(object):
    def __init__(self, input, output):
        self.__instruction_set = [
            PushInstruction(),
            LoadInstruction(),
            PopInstruction(),
            SwapInstruction(),
            AddInstruction(),
            SubInstruction(),
            MulInstruction(),
            DivInstruction(),
            JumpInstruction(),
            CallInstruction(),
            RetInstruction(),
            JEInstruction(),
            JSEInstruction(),
            ReadInstruction(input),
            WriteInstruction(output)
        ]

        self.__opcode_set = {}

        for instruction in self.__instruction_set:
            for opcode in instruction.generate_opcodes():
                self.__opcode_set[opcode.value] = opcode

    def decode(self, opcode):
        try:
            return self.__opcode_set[opcode]
        except KeyError:
            raise OpcodeError(opcode)


class OpcodeError(Exception):
    def __init__(self, opcode):
        self.opcode = opcode
        super(OpcodeError, self).__init__(hex(self.opcode) + ' is not known')


class MachineStack(object):
    def __init__(self, lst=()):
        self.__list = list(lst)

    def push(self, value):
        if value > 0xFF or value < 0:
            raise ArithmeticError("Cannot contain non-byte values")
        self.__list.append(value)

    def pop(self):
        return self.__list.pop()

    def copy(self):
        return MachineStack(self.__list)

    def __getitem__(self, item):
        return self.__list[-item-1]

    def __setitem__(self, key, value):
        if value > 0xFF or value < 0:
            raise ArithmeticError("Cannot contain non-byte values")
        self.__list[-key-1] = value

    def clear(self):
        self.__list = []

    def empty(self):
        return len(self.__list) == 0

    def __iter__(self):
        return iter(reversed(self.__list))

    def __len__(self):
        return len(self.__list)


class Machine(object):
    def __init__(self, code, input, output, stack=None):
        self.code = code
        self.stack = stack if stack is not None else MachineStack()
        self.instruction_set = InstructionSet(input, output)
        self.opcodes = map(self.instruction_set.decode, code)
        self.ip = 0

    def run(self):
        while 0 <= self.ip < len(self.code):
            op = self.opcodes[self.ip]
            #display_opcode(self.ip, op)
            #print self.dump_stack(ascii=False)
            self.ip += 1
            op.run(machine=self)

    def dump_stack(self, ascii=False):
        stack_data = ''

        if ascii:
            for b in self.stack:
                stack_data += chr(b) + ' '
        else:
            for b in self.stack:
                stack_data += hex(b) + ' '
        return stack_data


class HackingIO(object):
    def __init__(self):
        #self.flag_chars = [102, 108, 97, 103, 123, 88, 79, 82, 82,
        #          79, 76, 108, 73, 110, 71, 82, 48, 108,
        #
        #          108, 33, 110, 103, 82, 111, 76, 76, 33,
        #          110, 71, 82, 111, 108, 76, 73, 64, 223]

        self.flag_chars = []
        self.current = 9
        self.machine = None

    def flag(self):
        k = ''

        for c in self.flag_chars:
            k += chr(c)

        return k

    def remove(self):
        while True:
            self.current = self.flag_chars.pop()
            self.current += 1
            while self.current < 0xff and chr(self.current) not in string.printable:
                self.current += 1

            if self.current >= 0xff:
                continue

            return
    
    def read(self, n):
        self.stack = self.machine.stack.copy()

        if n != 1:
            raise Exception

        self.flag_chars.append(self.current)

        current_char = self.current

        self.current = 9

        return current_char

    def write(self, b):
        # Ignore writes
        pass


def debug(code):
    machine = Machine(code, sys.stdin, sys.stdout)
    breakpoints = []

    while True:
        cmd = raw_input('>> ')
        cmd = cmd.split(' ')

        if cmd[0] == 'exit':
            break

        elif cmd[0] == 'break':
            breakpoints.append(int(cmd[1], 16))

        elif cmd[0] == 'del':
            if cmd[1] == '*':
                breakpoints = []
            address = int(cmd[1], 16)
            breakpoints.remove(address)

        elif cmd[0] == 'stack':
            print machine.dump_stack(ascii='--ascii' in cmd)

        elif cmd[0] == 'state':
            print 'IP = ', hex(machine.ip)
            print 'StackSize = ', len(machine.stack)

        elif cmd[0] == 'next':
            opcode = machine.opcodes[machine.ip]
            display_opcode(machine.ip, opcode)
            machine.ip += 1
            opcode.run(machine)

        elif cmd[0] == 'list':
            if len(cmd) > 1:
                n = int(cmd[1])
            else:
                n = 10

            for ip in xrange(machine.ip, machine.ip+n):
                display_opcode(ip, machine.opcodes[ip])

        elif cmd[0] == 'continue':
            while 0 <= machine.ip <= 0xFF:
                if machine.ip in breakpoints:
                    print 'hit breakpoint at ', hex(machine.ip)
                    break

                opcode = machine.opcodes[machine.ip]
                machine.ip += 1
                opcode.run(opcode, machine)


def hack(code):
    stack = MachineStack()
    io = HackingIO()
    machine = Machine(code, io, io, stack)
    io.machine = machine

    i = 0

    while True:
        try:
            machine.run()
        except Exception as e:
            print str(e)
            traceback.print_exc()
            print io.flag()
            break

        i += 1

        if i % 1000 == 0:
            print io.flag_chars

        if machine.stack.empty():
            print io.flag()
            break

        io.remove()
        machine.ip = 0x28
        machine.stack = io.stack.copy()


def display_opcode(ip, opcode):
    print "0x%02x 0x%02x" % (ip, opcode.value), str(opcode)


def decompile(code):
    ins = InstructionSet(None, None)

    for ip, opcode in enumerate(map(ins.decode, code)):
        display_opcode(ip, opcode)


def run(code):
    machine = Machine(code, sys.stdin, sys.stdout)
    machine.run()


def main():

    with open('machine.bin', 'rb') as f:
        code = f.read()
        code = map(ord, code)

    if '--run' in sys.argv:
        run(code)

    elif '--decompile' in sys.argv:
        decompile(code)

    elif '--debug' in sys.argv:
        debug(code)

    elif '--hack' in sys.argv:
        hack(code)

main()
