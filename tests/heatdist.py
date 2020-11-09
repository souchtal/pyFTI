from mpi4py import MPI
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fti import *


# here goes the test
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

configFile = sys.argv[1]

res = FTI_Init(configFile, comm)
print("initialized"+str(res))
