"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # Allocates 256 bytes of memory
        self.reg = [0] * 8
        self.pc = 0 # Program counter/accumalator

        ########## INSTRUCTION HANDLERS ##########
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010

    def load(self):
        """Load a program into memory."""
        # Check to see if there are two arguments
        # Second argument must be the filename of program to load
        if len(sys.argv) != 2:
            print('Usage: file.py <filename>', file=sys.stderr)
            sys.exit(1)

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    # Ignore comments
                    comment_split = line.split('#')
                    num = comment_split[0].strip()
                    
                    if num == '':
                        # Ignore blank lines
                        continue
                    
                    value = int(num, 2)
                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found.')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # Memory Address Register (MAR) refers to the address that is being read/written to
    def ram_read(self, MAR):
        return self.ram[MAR]

    # Memory Data Register (MDR) refers to the data that was read/data to write
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""

        while True:
            # Instruction Register (IR)
            IR = self.ram_read(self.pc)

            # Set the value of a register to an integer.
            if IR is self.LDI:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b
                self.pc += 3
            # Multiply the values in two registers together and store the result in registerA
            elif IR is self.MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
                self.pc += 3
            # Print to the console the decimal integer value that is stored in the given register.
            elif IR is self.PRN:
                print(self.reg[operand_a])
                self.pc += 2
            # Halt the CPU (and exit the emulator)
            elif IR is self.HLT:
                break
            else:
                print(f'Error: Unknown command: {IR}')
                sys.exit(1)