# *-* coding: utf-8 -*-

# MPI code for finding prime numbers on a specific given range
# Author: William Gambardella

# Use: mpirun -np 4 -machinefile ../api/machinefile python primes.py -n nceiling

from mpi4py import MPI as mpi
import numpy as np
import sys
import math

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def vectorSize(numOfProcesses,sequenceSize, rankNumber):
    nop = float(numOfProcesses)
    seqsize = float(sequenceSize)

    remainder = seqsize%nop

    if remainder == 0:
        return seqsize/nop
    else:
        if rankNumber < remainder:
            return math.ceil(seqsize/nop)
        else:
            return math.floor(seqsize/nop)

def isPrime(workingSieve, primeFactor):
    primeVector = []

    for pos in range(0,len(workingSieve)):
        if workingSieve[pos] == primeFactor:
            primeVector.append(workingSieve[pos])
        elif workingSieve[pos]%primeFactor != 0:
            primeVector.append(workingSieve[pos])

    return primeVector

print "I'm process number %d" % rank

nceiling = None
mainSieve = None
workerSieve = None
workerSieveBuffer = None
msBuffer = None
resultBuffer = []
resultBufferSize = 0
displs = []
counts = []
pfactor = 2
returnVecLength = 0
returnSizes = []
receiveDispls = []
returnBuffer = None

startTime = mpi.Wtime() # Starts the MPI process clock

if rank==0:
    cmdargs = sys.argv
    nceiling = int(cmdargs[2])
    mainSieve = np.arange(2,nceiling+1,dtype=np.float)

nceiling = comm.bcast(nceiling, root=0) # Broadcast the input number

if rank == 0:
    for x in range(0,size):
        counts.append(int(vectorSize(size,nceiling-1,x)))
        if x == 0:
            displs.append(0)
        else:
            displs.append(counts[x-1]+displs[x-1])

    counts = tuple(counts)
    displs = tuple(displs)

workerSieve = np.zeros(vectorSize(size,nceiling-1,rank))
workerSieveBuffer = np.getbuffer(np.zeros(vectorSize(size,nceiling-1,rank)))
comm.Barrier()

if rank == 0:
    msBuffer = buffer(mainSieve)

comm.Scatterv([msBuffer,counts,displs,mpi.DOUBLE],workerSieveBuffer, root=0)

resultBuffer = np.frombuffer(workerSieveBuffer)

while(pfactor*pfactor <= nceiling):
    resultBuffer = isPrime(resultBuffer, pfactor)
    comm.Barrier()
    pfactor += 1

returnVecLength = comm.allreduce(len(resultBuffer), op=mpi.SUM)

returnSizes = comm.allgather(len(resultBuffer))

for y in range(0,size):
    if y == 0:
        receiveDispls.append(0)
    else:
        receiveDispls.append(returnSizes[y-1]+receiveDispls[y-1])

returnBuffer = np.getbuffer(np.zeros(returnVecLength))

comm.Gatherv(np.getbuffer(np.asarray(resultBuffer)),[returnBuffer,tuple(returnSizes),tuple(receiveDispls),mpi.DOUBLE], root=0)

if rank == 0:
    returnBuffer = np.frombuffer(returnBuffer)
    endTime = mpi.Wtime()
    print returnBuffer
    print "I took %f seconds to do it all." % (endTime-startTime)
