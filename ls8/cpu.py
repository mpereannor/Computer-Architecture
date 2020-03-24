"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #hold 256 bytes of memory 
        self.ram = [0] * 256
        #8 general purpose registers
        self.reg = [0] * 8
        #internal registers
        self.pc  = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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

    def run(self):
        """Run the CPU."""
        #read bytes at pc1 & pc2 from ram into op_a & op_b
        #set operand_a to pc+1
        op_a = self.ram_read(self.pc + 1)
        #set operand_b to pc+2
        op_b = self.ram_read(self.pc + 2)
        
        #create instructions for LDI, PRN, HLT programs
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        
        running = True
        
        #while cpu is running 
        while running:
          #set instruction register to read memory address stored in register pc
          IR = self.ram[self.pc]
          if IR == HLT:
            running = False
          elif IR == LDI:
            self.ram_write(op_a, op_b)
            #or self.reg[op_a] = op_b
            self.pc += 3
          elif IR == PRN:
            print(op_b)
            #or print(self.reg[op_a])
            self.pc += 2
        
        
    #helper function
    def ram_read(self, MAR): #Memory Address Register (MAR)
      return self.ram[MAR]
    
    def ram_write(self, MAR, MDR): #Memory Data Register (MDR)
      self.reg[MAR] = MDR
