#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) < 2: 
  print("usage: ls8.py progname")
  sys.exit(1)

cpu.load()
cpu.run()