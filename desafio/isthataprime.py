# *-* coding: utf-8 -*-

# MPI code for finding prime numbers on a specific given range
# Author: William Gambardella

# Use: mpirun -np 4 -machinefile ../api/machinefile python isthataprime.py -n nceiling

from mpi4py import MPI as mpi
import numpy as np
import sys
import math

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def isPrime(assignedPrime):
    p = 3
    if assignedPrime % 2 == 0:
        return False
    else:
        while (p*p) <= assignedPrime:
            if assignedPrime%p == 0:
                return False
            else:
                p = p+2
    return True

myPrime = None
boolPrime = False
primeVector = None
answer = ""
attempts = []

if rank == 0:
    primeFile = open('primeNumbers.txt','r')
    primeString = primeFile.read()
    primeVector = ' '.join(primeString.split('\n')).split(' ')
    del primeVector[-1]
    print primeVector

myPrime = comm.scatter(primeVector, myPrime, root=0)

print ("I'm process %s and I've received %s as my prime number" % (rank,myPrime))

for x in range(0,4):
    startTime = mpi.Wtime()

    boolPrime = isPrime(int(myPrime))

    endTime = mpi.Wtime()

    attempts.append(endTime-startTime)

    if boolPrime != True:
        answer = "not"

    print ("Process %s: %s is %s a prime number.'\n'I took %f seconds." % (rank,myPrime,answer,(endTime-startTime)))

print attempts
