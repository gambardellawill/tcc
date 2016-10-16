# *-* coding: utf-8 -*-

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

    """for position in range(0,len(workingSieve)):
        if workingSieve[position]%2 == 0:
            primeVector.append(0)
        else:
            primeFactor = 3
            while (primeFactor*primeFactor) <= workingSieve[position]:
                if workingSieve[position]%primeFactor == 0:
                    primeVector.append(0)
                else:
                    primeFactor += 2
            primeVector.append(workingSieve[position])
        print primeVector"""

    for pos in range(0,len(workingSieve)):
        if workingSieve[pos] == 2:
            primeVector.append(workingSieve[pos])
        elif workingSieve[pos]%2 != 0:
            primeVector.append(workingSieve[pos])

    print primeVector
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

if rank==0:
    cmdargs = sys.argv
    nceiling = int(cmdargs[2])
    mainSieve = np.arange(2,nceiling+1,dtype=np.float)

nceiling = comm.bcast(nceiling, root=0)
print "I'm process number %d and the ceiling number is %d" % (rank,nceiling)

if rank == 0:
    for x in range(0,size):
        counts.append(int(vectorSize(size,nceiling-1,x)))
        if x == 0:
            displs.append(0)
        else:
            displs.append(counts[x-1]+displs[x-1])

    counts = tuple(counts)
    #print counts

    displs = tuple(displs)
    #print displs

workerSieve = np.zeros(vectorSize(size,nceiling-1,rank))
workerSieveBuffer = np.getbuffer(np.zeros(vectorSize(size,nceiling-1,rank)))

comm.Barrier()

if rank == 0:
    msBuffer = buffer(mainSieve)

comm.Scatterv([msBuffer,counts,displs,mpi.DOUBLE],workerSieveBuffer, root=0)

workerSieve = np.frombuffer(workerSieveBuffer)

resultBuffer = isPrime(workerSieve, 2)

pfactorn = resultBuffer[0]
if pfactorn == pfactor:
    pfactorn = resultBuffer[1]

pfactorn = comm.allreduce(pfactorn,op=mpi.MIN)
