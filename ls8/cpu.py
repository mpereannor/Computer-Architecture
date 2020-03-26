"""CPU functionality."""

import sys

#create instructions for LDI, PRN, and HLT programs
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
  """Main CPU Class"""
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
    self.branchtable = {}
    self.branchtable[HLT] = self.handle_hlt
    self.branchtable[LDI] = self.handle_ldi
    self.branchtable[PRN] = self.handle_prn
    self.branchtable[MUL] = self.handle_mul
    
  #helper functions
  def ram_read(self, MAR): #Memory Address Register (MAR)
    return self.ram[MAR]
  
  # def ram_write(self, MAR, MDR): #Memory Data Register (MDR)
    # self.reg[MAR] = MDR
    
  def ram_write(self, MDR, value):
    self.ram[MDR] = value
    
  def load(self):
    if len(sys.argv) != 2:
      print("format: ls8.py [filename]")
      sys.exit(1)
    
    program = sys.argv[1]
    address = 0
    
    #open file
    with open(program) as f:
      #read the lines
      for line in f: 
        #parse out comments
        line = line.strip().split("#")[0]
        #cast numbers from strings to int 
        val = line.strip()
        #ignore blank lines
        if line == "":
          continue 
        
        value = int(val, 2)
        self.ram[address] = value
        address += 1
        
  def alu(self, op, reg_a, reg_b):
    """ALU operations"""
    if op == "ADD":
      self.reg[reg_a] += self.reg[reg_b]
    
    elif op == "MUL":
      self.reg[reg_a] *= self.reg[reg_b]
    
    else:
      raise Exception("Unsurpported ALU operation")
  
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
  
  def handle_ldi(self):
    operand_a = self.ram_read(self.pc + 1)
    operand_b = self.ram_read(self.pc + 2)
    
    self.reg[operand_a] = operand_b
    
  def handle_prn(self):
    operand_a = self.ram_read(self.pc + 1)
    print(self.reg[operand_a])
    
  def handle_hlt(self):
    self.halted = True
    
  def handle_mul(self):
    operand_a = self.ram_read(self.pc + 1)
    operand_b = self.ram_read(self.pc + 2)
    self.alu("MUL", operand_a, operand_b)
  
  def run(self):
    while self.running:
      IR = self.ram[self.pc]
      val = IR
      op_count = val >> 6
      IR_length = op_count + 1
      self.branchtable[IR]()
      
      if IR == 0 or None:
        print(f'Unknown instructions and index {self.pc}')
        sys.exit(1)
      self.pc += IR_length
 
              
          


  