# *-* coding: utf-8 -*-

# MPI code for finding prime numbers on a specific given range
# Author: William Gambardella

# Use: mpirun -np 4 -machinefile ../api/machinefile python isthataprime.py -n nceiling

from mpi4py import MPI as mpi
import numpy as np
import socket

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

hostname = socket.gethostname()

print ("%s - process %d" % (hostname,rank)) 
