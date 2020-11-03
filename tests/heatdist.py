from mpi4py import MPI
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fti import *

# here goes the test
FTI_Init()
typef = FTIT_type()
typef.size=1887

print(typef.size)