"""CPU functionality."""

import sys

#create instructions for LDI, PRN, and HLT programs
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010


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
        #activate loop
        self.running = False
        self.ir = None
        
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        
        
        
        
        

    def load(self, progname):
        """Load a program into memory."""
        """
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

        """
        try:
          address = 0
          self.running = True
          with open(progname, 'r') as f:
            #read the lines
            for line in f:
              #split line before and after comment symbol
              line = line.split("#")[0]
              #extract number
              line = line.strip() #lose whitespace
              #ignore blank lines
              if line == '':
                continue
              if len(line) > 0:
                #convert our binary string to a number
                val = int(line, 2)
                #store val at address in memory 
                self.ram_write(val, address)
                address += 1
                
        except FileNotFoundError:
          print(f'{sys.argv[0]}: {progname} not found')
          sys.exit(2)
                
              
          


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        if op == "MUL":
          self.reg[reg_a] *= self.reg[reg_b]
          
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
        
        # running = True
        
        #while cpu is running 
        while self.running:
          # #set instruction register to read memory address stored in register pc
          # IR = self.ram[self.pc]
          # if IR == HLT:
          #   running = False
          # elif IR == LDI:
          #   self.ram_write(op_a, op_b)
          #   #or self.reg[op_a] = op_b
          #   self.pc += 3
          # elif IR == PRN:
          #   print(op_b)
          #   #or print(self.reg[op_a])
          #   self.pc += 2
          
          #get instruction from ram 
          ram_read_ins= self.ram_read(self.pc)
          self.ir = ram_read_ins
          
          if ram_read_ins == 0b00000001:
            self.running  = False
            exit()
          format_ram_read_ins = '{0:8b}'.format(ram_read_ins)
          num_op = int(format_ram_read_ins[:2].strip() or '00', 2)
          alu_op = int(format_ram_read_ins[2].strip() or '0', 2)
          inst_set = int(format_ram_read_ins[3].strip() or '0', 2)
          inst_iden = int(format_ram_read_ins[4:].strip() or '000', 2)
          
          if alu_op == int('1', 2):
            self.alu('MUL', self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            
            #Print output 
            self.pc += int(num_op) + 1
            
          else:
            if ram_read_ins == 0b10000010:
              key = int(self.ram_read(self.pc + 1))
              value = self.ram_read(self.pc + 2)
              self.reg[key] = value 
              self.pc += int(num_op) + 1
            
            elif ram_read_ins  == 0b01000111:
              key = int(self.ram_read(self.pc + 2))
              print(int(self.reg[key]))
              self.pc += int(num_op) + 1
          
          
        
        
    #helper function
    def ram_read(self, MAR): #Memory Address Register (MAR)
      return self.ram[MAR]
    
    def ram_write(self, MAR, MDR): #Memory Data Register (MDR)
      self.reg[MAR] = MDR
